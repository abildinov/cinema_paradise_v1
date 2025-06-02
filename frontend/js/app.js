const { useState, useEffect } = React;

// Простой роутер
class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = '/';
    }
    
    navigate(route) {
        this.currentRoute = route;
        window.dispatchEvent(new CustomEvent('routeChanged', { detail: route }));
    }
}

window.router = new Router();

function App() {
    // Проверка доступности компонентов
    console.log('App: Checking component availability:', {
        BookingModal: !!window.BookingModal,
        SessionCard: !!window.SessionCard,
        LoginModal: !!window.LoginModal
    });
    
    const [movies, setMovies] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);
    const [showLoginModal, setShowLoginModal] = useState(false);
    const [showBookingModal, setShowBookingModal] = useState(false);
    const [showUserProfile, setShowUserProfile] = useState(false);
    const [showAdminPanel, setShowAdminPanel] = useState(false);
    const [selectedSession, setSelectedSession] = useState(null);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [currentRoute, setCurrentRoute] = useState('/');

    useEffect(() => {
        initializeApp();
        
        // Слушаем события роутера
        const handleRouteChange = (e) => {
            setCurrentRoute(e.detail);
        };
        
        // Слушаем событие открытия модального окна
        const handleOpenLoginModal = () => {
            setShowLoginModal(true);
        };
        
        // Слушаем событие открытия профиля
        const handleOpenUserProfile = () => {
            setShowUserProfile(true);
        };
        
        // Слушаем событие открытия админ панели
        const handleOpenAdminPanel = () => {
            setShowAdminPanel(true);
        };
        
        // Слушаем изменения в localStorage (когда пользователь авторизуется в другой вкладке)
        const handleStorageChange = () => {
            checkAuthentication();
        };
        
        // Слушаем ошибки авторизации
        const handleAuthError = () => {
            setUser(null);
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        };
        
        window.addEventListener('routeChanged', handleRouteChange);
        window.addEventListener('openLoginModal', handleOpenLoginModal);
        window.addEventListener('openUserProfile', handleOpenUserProfile);
        window.addEventListener('openAdminPanel', handleOpenAdminPanel);
        window.addEventListener('storage', handleStorageChange);
        window.addEventListener('authError', handleAuthError);
        
        return () => {
            window.removeEventListener('routeChanged', handleRouteChange);
            window.removeEventListener('openLoginModal', handleOpenLoginModal);
            window.removeEventListener('openUserProfile', handleOpenUserProfile);
            window.removeEventListener('openAdminPanel', handleOpenAdminPanel);
            window.removeEventListener('storage', handleStorageChange);
            window.removeEventListener('authError', handleAuthError);
        };
    }, []);

    const checkAuthentication = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const userData = await window.api.getCurrentUser();
                setUser(userData);
            } catch (error) {
                console.log('Token validation failed:', error);
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                setUser(null);
            }
        } else {
            setUser(null);
        }
    };

    const initializeApp = async () => {
        try {
            setLoading(true);
            
            // Проверяем аутентификацию
            await checkAuthentication();

            // Загружаем демо данные
            try {
                await window.api.populateDemo();
                console.log('Demo data populated');
            } catch (error) {
                console.log('Demo data already exists or error:', error.message);
            }

            // Загружаем фильмы и сеансы
            const [moviesData, sessionsData] = await Promise.all([
                window.api.getMovies(),
                window.api.getSessions()
            ]);

            setMovies(moviesData || []);
            setSessions(sessionsData || []);
            
        } catch (error) {
            console.error('App initialization error:', error);
            setError('Ошибка загрузки данных: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleLoginSuccess = async (userData) => {
        console.log('Login success:', userData);
        setUser(userData);
        setShowLoginModal(false);
        setError('');
        
        // Обновляем данные после авторизации
        try {
            const [moviesData, sessionsData] = await Promise.all([
                window.api.getMovies(),
                window.api.getSessions()
            ]);
            setMovies(moviesData || []);
            setSessions(sessionsData || []);
        } catch (err) {
            console.error('Error refreshing data after login:', err);
        }
    };

    const handleLogout = () => {
        window.AuthUtils.logout();
        setUser(null);
    };

    const handleBooking = (session) => {
        console.log('App: handleBooking called with session:', session);
        console.log('App: Current user:', user);
        
        if (!user) {
            console.log('App: No user, showing login modal');
            setShowLoginModal(true);
            return;
        }
        
        console.log('App: Setting selected session and showing booking modal');
        setSelectedSession(session);
        setShowBookingModal(true);
    };

    const handleBookingSuccess = (booking) => {
        setShowBookingModal(false);
        setSelectedSession(null);
        
        // Показываем уведомление о успешном бронировании
        if (booking && booking.seat_numbers) {
            setSuccessMessage(`🎉 Билет успешно забронирован! Места: ${booking.seat_numbers.join(', ')}, Сумма: ${booking.total_price} ₽`);
        } else {
            setSuccessMessage('🎉 Билет успешно забронирован!');
        }
        
        // Автоматически скрываем уведомление через 5 секунд
        setTimeout(() => setSuccessMessage(''), 5000);
        
        // Обновляем сеансы
        window.api.getSessions().then(setSessions).catch(console.error);
    };

    if (loading) {
        return React.createElement('div', {
            className: 'min-h-screen bg-gray-900 flex items-center justify-center'
        },
            React.createElement('div', {
                className: 'text-center'
            },
                React.createElement('div', {
                    className: 'text-6xl mb-4'
                }, '🎬'),
                React.createElement('div', {
                    className: 'text-white text-xl'
                }, 'Загрузка Cinema Paradise...'),
                React.createElement(window.LoadingSpinner, { size: 'large' })
            )
        );
    }

    return React.createElement('div', {
        className: 'min-h-screen bg-gray-900'
    },
        // Header
        React.createElement(window.Header),
        
        // Error Alert
        error && React.createElement(window.Alert, {
            type: 'error',
            message: error,
            onClose: () => setError('')
        }),

        // Success Alert
        successMessage && React.createElement(window.Alert, {
            type: 'success',
            message: successMessage,
            onClose: () => setSuccessMessage('')
        }),

        // Main Content
        React.createElement('main', {
            className: 'container mx-auto px-4 py-8'
        },
            // Hero Section
            React.createElement('section', {
                className: 'cinema-theme rounded-2xl p-8 text-center mb-12'
            },
                React.createElement('h2', {
                    className: 'text-4xl font-bold text-white mb-4'
                }, '🎭 Добро пожаловать в Cinema Paradise!'),
                React.createElement('p', {
                    className: 'text-xl text-purple-200 mb-6'
                }, 'Окунитесь в мир кинематографа')
            ),

            // Movies Section
            React.createElement('section', {
                className: 'mb-12'
            },
                React.createElement('h2', {
                    className: 'text-3xl font-bold text-white mb-8 text-center'
                }, '🎬 Фильмы в прокате'),
                React.createElement('div', {
                    className: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                },
                    movies.map(movie => 
                        React.createElement(window.MovieCard, {
                            key: movie.id,
                            movie: movie,
                            onSelect: (movie) => console.log('Selected movie:', movie)
                        })
                    )
                )
            ),

            // Sessions Section
            React.createElement('section', null,
                React.createElement('h2', {
                    className: 'text-3xl font-bold text-white mb-8 text-center'
                }, '🎭 Ближайшие сеансы'),
                
                // Отладочная информация
                React.createElement('div', {
                    className: 'text-white text-sm mb-4 text-center opacity-70'
                }, `Загружено сеансов: ${sessions.length}, Показано: ${Math.min(sessions.length, 6)}`),
                
                React.createElement('div', {
                    className: 'grid grid-cols-1 md:grid-cols-2 gap-6'
                },
                    sessions.length === 0 ? 
                        React.createElement('div', {
                            className: 'col-span-full text-center text-gray-400 py-8'
                        }, 'Сеансы загружаются...') :
                        sessions.slice(0, 6).map((session, index) => {
                            console.log(`Rendering session ${index}:`, session);
                            return React.createElement(window.SessionCard, {
                                key: session.id,
                                session: session,
                                onBook: handleBooking
                            });
                        })
                )
            )
        ),

        // Footer
        React.createElement('footer', {
            className: 'bg-gray-800 border-t border-gray-700 mt-16'
        },
            React.createElement('div', {
                className: 'container mx-auto px-4 py-8 text-center'
            },
                React.createElement('div', {
                    className: 'text-2xl mb-4'
                }, '🎬'),
                React.createElement('h3', {
                    className: 'text-xl font-bold text-white mb-2'
                }, 'Cinema Paradise'),
                React.createElement('p', {
                    className: 'text-gray-400 mb-4'
                }, 'Лучший кинотеатр города с современными технологиями'),
                React.createElement('div', {
                    className: 'text-gray-500'
                }, '© 2024 Cinema Paradise. Создано с ❤️ для лучшего кино опыта')
            )
        ),

        // Debug BookingModal state
        console.log('App: Rendering BookingModal with state:', {
            showBookingModal,
            hasSelectedSession: !!selectedSession,
            selectedSessionId: selectedSession?.id,
            BookingModalExists: !!window.BookingModal,
            willRenderBookingModal: showBookingModal && selectedSession
        }),

        // Modals
        React.createElement(window.LoginModal, {
            isOpen: showLoginModal,
            onClose: () => setShowLoginModal(false),
            onSuccess: handleLoginSuccess
        }),

        React.createElement(window.BookingModal, {
            isOpen: showBookingModal,
            session: selectedSession,
            onClose: () => setShowBookingModal(false),
            onSuccess: handleBookingSuccess
        }),

        showUserProfile && React.createElement(window.UserProfile, {
            user: user,
            onClose: () => setShowUserProfile(false)
        }),

        showAdminPanel && React.createElement(window.AdminPanel, {
            user: user,
            onClose: () => setShowAdminPanel(false)
        })
    );
}

// Render the app with React 18 createRoot
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));