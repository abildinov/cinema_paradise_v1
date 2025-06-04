// Header Component
const Header = () => {
    const [user, setUser] = React.useState(null);

    React.useEffect(() => {
        checkAuthentication();
        
        // Подписываемся на события логина/логаута
        const handleStorageChange = () => {
            checkAuthentication();
        };
        
        // Обработчик успешного логина
        const handleLoginSuccess = () => {
            checkAuthentication();
        };
        
        // Обработчик ошибки авторизации
        const handleAuthError = () => {
            setUser(null);
        };
        
        window.addEventListener('storage', handleStorageChange);
        window.addEventListener('loginSuccess', handleLoginSuccess);
        window.addEventListener('authError', handleAuthError);
        
        return () => {
            window.removeEventListener('storage', handleStorageChange);
            window.removeEventListener('loginSuccess', handleLoginSuccess);
            window.removeEventListener('authError', handleAuthError);
        };
    }, []);
    
    const checkAuthentication = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                // Проверяем токен через API
                const userData = await window.api.getCurrentUser();
                setUser(userData);
            } catch (e) {
                // Недействительный токен
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                setUser(null);
            }
        } else {
            setUser(null);
        }
    };

    const handleLogout = () => {
        window.AuthUtils.logout();
        setUser(null);
    };

    const openLoginModal = () => {
        window.showLoginModal();
    };

    return React.createElement('header', {
        className: 'bg-gray-900/95 backdrop-blur-sm border-b border-purple-500/20 sticky top-0 z-50'
    },
        React.createElement('div', {
            className: 'container mx-auto px-4 py-4'
        },
            React.createElement('div', {
                className: 'flex justify-between items-center'
            },
                React.createElement('div', {
                    className: 'flex items-center space-x-6'
                },
                    React.createElement('h1', {
                        className: 'text-2xl font-bold text-white cursor-pointer hover:text-purple-400 transition-colors',
                        onClick: () => window.router.navigate('/')
                    }, '🎬 CinemaAPI'),
                    React.createElement('nav', {
                        className: 'hidden md:flex space-x-6'
                    },
                        React.createElement('button', {
                            className: 'text-gray-300 hover:text-white transition-colors',
                            onClick: () => window.router.navigate('/')
                        }, 'Главная'),
                        React.createElement('button', {
                            className: 'text-gray-300 hover:text-white transition-colors',
                            onClick: () => window.router.navigate('/movies')
                        }, 'Фильмы'),
                        React.createElement('button', {
                            className: 'text-gray-300 hover:text-white transition-colors',
                            onClick: () => window.router.navigate('/sessions')
                        }, 'Сеансы')
                    )
                ),
                React.createElement('div', {
                    className: 'flex items-center space-x-4'
                },
                    // Auth buttons
                    user ? React.createElement('div', {
                        className: 'flex items-center gap-4'
                    },
                        React.createElement('span', {
                            className: 'text-white'
                        }, `Привет, ${user.username}!`),
                        
                        // Profile button
                        React.createElement('button', {
                            className: 'text-white hover:text-purple-200 transition-colors flex items-center gap-2',
                            onClick: () => window.dispatchEvent(new CustomEvent('openUserProfile'))
                        },
                            React.createElement('span', null, '👤'),
                            React.createElement('span', {
                                className: 'hidden md:inline'
                            }, 'Профиль')
                        ),
                        
                        // Admin panel button (only for admins)
                        user.role === 'admin' && React.createElement('button', {
                            className: 'text-white hover:text-purple-200 transition-colors flex items-center gap-2',
                            onClick: () => window.dispatchEvent(new CustomEvent('openAdminPanel'))
                        },
                            React.createElement('span', null, '👑'),
                            React.createElement('span', {
                                className: 'hidden md:inline'
                            }, 'Админ')
                        ),
                        
                        React.createElement('button', {
                            className: 'bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors',
                            onClick: handleLogout
                        }, 'Выйти')
                    ) : React.createElement('button', {
                        className: 'bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors',
                        onClick: openLoginModal
                    }, 'Войти')
                )
            )
        )
    );
};

window.Header = Header;