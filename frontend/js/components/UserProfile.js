// User Profile Component
const UserProfile = ({ user, onClose }) => {
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (user) {
            loadUserTickets();
        }
    }, [user]);

    const loadUserTickets = async () => {
        try {
            setLoading(true);
            const response = await window.api.getUserTickets();
            setTickets(response || []);
        } catch (error) {
            console.error('Error loading user tickets:', error);
            setError('Ошибка загрузки билетов: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'active': return 'text-green-600 bg-green-100';
            case 'used': return 'text-gray-600 bg-gray-100';
            case 'cancelled': return 'text-red-600 bg-red-100';
            case 'pending': return 'text-yellow-600 bg-yellow-100';
            default: return 'text-blue-600 bg-blue-100';
        }
    };

    const getStatusText = (status) => {
        switch (status) {
            case 'active': return 'Активен';
            case 'used': return 'Использован';
            case 'cancelled': return 'Отменен';
            case 'pending': return 'Ожидает подтверждения';
            default: return status;
        }
    };

    return React.createElement('div', {
        className: 'fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm'
    },
        React.createElement('div', {
            className: 'bg-white rounded-2xl shadow-2xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden'
        },
            // Header
            React.createElement('div', {
                className: 'cinema-theme p-6 text-white'
            },
                React.createElement('div', {
                    className: 'flex justify-between items-center'
                },
                    React.createElement('div', null,
                        React.createElement('h2', {
                            className: 'text-2xl font-bold mb-2'
                        }, '👤 Личный кабинет'),
                        React.createElement('p', {
                            className: 'text-purple-200'
                        }, `Добро пожаловать, ${user?.username || 'Пользователь'}!`)
                    ),
                    React.createElement('button', {
                        className: 'text-3xl hover:bg-white/20 w-10 h-10 rounded-full flex items-center justify-center transition-colors',
                        onClick: onClose
                    }, '×')
                )
            ),

            // Content
            React.createElement('div', {
                className: 'p-6 overflow-y-auto max-h-[60vh]'
            },
                // User Info Section
                React.createElement('div', {
                    className: 'bg-gray-50 rounded-lg p-4 mb-6'
                },
                    React.createElement('h3', {
                        className: 'text-lg font-semibold mb-4 text-gray-800'
                    }, '📋 Информация о профиле'),
                    React.createElement('div', {
                        className: 'grid grid-cols-1 md:grid-cols-2 gap-4'
                    },
                        React.createElement('div', null,
                            React.createElement('label', {
                                className: 'block text-sm font-medium text-gray-600 mb-1'
                            }, 'Имя пользователя'),
                            React.createElement('p', {
                                className: 'text-gray-900 font-medium'
                            }, user?.username || '-')
                        ),
                        React.createElement('div', null,
                            React.createElement('label', {
                                className: 'block text-sm font-medium text-gray-600 mb-1'
                            }, 'Email'),
                            React.createElement('p', {
                                className: 'text-gray-900 font-medium'
                            }, user?.email || '-')
                        ),
                        React.createElement('div', null,
                            React.createElement('label', {
                                className: 'block text-sm font-medium text-gray-600 mb-1'
                            }, 'Роль'),
                            React.createElement('span', {
                                className: `inline-block px-3 py-1 rounded-full text-sm font-medium ${
                                    user?.role === 'admin' ? 'bg-red-100 text-red-800' :
                                    user?.role === 'manager' ? 'bg-yellow-100 text-yellow-800' :
                                    'bg-blue-100 text-blue-800'
                                }`
                            }, user?.role === 'admin' ? '👑 Администратор' :
                               user?.role === 'manager' ? '👔 Менеджер' : '👤 Клиент')
                        ),
                        React.createElement('div', null,
                            React.createElement('label', {
                                className: 'block text-sm font-medium text-gray-600 mb-1'
                            }, 'Всего билетов'),
                            React.createElement('p', {
                                className: 'text-gray-900 font-medium text-xl'
                            }, tickets.length)
                        )
                    )
                ),

                // Tickets Section
                React.createElement('div', null,
                    React.createElement('h3', {
                        className: 'text-lg font-semibold mb-4 text-gray-800'
                    }, '🎫 Мои билеты'),
                    
                    error && React.createElement('div', {
                        className: 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'
                    }, error),

                    loading ? React.createElement('div', {
                        className: 'text-center py-8'
                    },
                        React.createElement(window.LoadingSpinner),
                        React.createElement('p', {
                            className: 'text-gray-600 mt-2'
                        }, 'Загружаем ваши билеты...')
                    ) : tickets.length === 0 ? React.createElement('div', {
                        className: 'text-center py-8'
                    },
                        React.createElement('div', {
                            className: 'text-6xl mb-4'
                        }, '🎫'),
                        React.createElement('p', {
                            className: 'text-gray-600 text-lg'
                        }, 'У вас пока нет забронированных билетов'),
                        React.createElement('p', {
                            className: 'text-gray-500 mt-2'
                        }, 'Забронируйте билет на любой фильм!')
                    ) : React.createElement('div', {
                        className: 'space-y-4'
                    },
                        tickets.map(ticket => 
                            React.createElement('div', {
                                key: ticket.id,
                                className: 'border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow'
                            },
                                React.createElement('div', {
                                    className: 'flex justify-between items-start mb-3'
                                },
                                    React.createElement('div', null,
                                        React.createElement('h4', {
                                            className: 'font-semibold text-lg text-gray-900'
                                        }, ticket.session?.movie?.title || 'Неизвестный фильм'),
                                        React.createElement('p', {
                                            className: 'text-gray-600'
                                        }, `${ticket.session?.hall?.name || 'Неизвестный зал'}`)
                                    ),
                                    React.createElement('span', {
                                        className: `px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(ticket.is_confirmed ? 'active' : 'pending')}`
                                    }, getStatusText(ticket.is_confirmed ? 'active' : 'pending'))
                                ),
                                
                                React.createElement('div', {
                                    className: 'grid grid-cols-1 md:grid-cols-3 gap-4 text-sm'
                                },
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, '📅 Дата и время:'),
                                        React.createElement('br'),
                                        React.createElement('span', {
                                            className: 'font-medium'
                                        }, formatDate(ticket.session?.start_time))
                                    ),
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, '🪑 Место:'),
                                        React.createElement('br'),
                                        React.createElement('span', {
                                            className: 'font-medium'
                                        }, ticket.seat_number ? `Ряд ${ticket.row_number}, Место ${ticket.seat_number}` : 'Не указано')
                                    ),
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, '💰 Стоимость:'),
                                        React.createElement('br'),
                                        React.createElement('span', {
                                            className: 'font-medium text-green-600'
                                        }, `${ticket.price || 0} ₽`)
                                    )
                                )
                            )
                        )
                    )
                )
            ),

            // Footer
            React.createElement('div', {
                className: 'border-t border-gray-200 p-4 bg-gray-50'
            },
                React.createElement('div', {
                    className: 'flex justify-between items-center'
                },
                    React.createElement('p', {
                        className: 'text-gray-600 text-sm'
                    }, `Дата регистрации: ${user?.created_at ? formatDate(user.created_at) : 'Неизвестно'}`),
                    React.createElement('button', {
                        className: 'bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors',
                        onClick: onClose
                    }, 'Закрыть')
                )
            )
        )
    );
};

window.UserProfile = UserProfile; 