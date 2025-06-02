// Admin Panel Component
const AdminPanel = ({ user, onClose }) => {
    const [activeTab, setActiveTab] = useState('stats');
    const [stats, setStats] = useState(null);
    const [tickets, setTickets] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (user?.role === 'admin') {
            loadData();
        } else {
            setError('Доступ запрещен. Только для администраторов.');
        }
    }, [user, activeTab]);

    const loadData = async () => {
        try {
            setLoading(true);
            setError('');
            
            if (activeTab === 'stats') {
                // Загружаем статистику
                const [moviesData, sessionsData, ticketsData, usersData] = await Promise.all([
                    window.api.getMovies(),
                    window.api.getSessions(),
                    window.api.getAllTickets(),
                    window.api.getAllUsers()
                ]);
                
                setStats({
                    movies: moviesData?.length || 0,
                    sessions: sessionsData?.length || 0,
                    active_sessions: sessionsData?.filter(s => s.is_active)?.length || 0,
                    tickets: ticketsData?.length || 0,
                    users: usersData?.length || 0,
                    revenue: ticketsData?.reduce((sum, ticket) => sum + (ticket.price || 0), 0) || 0
                });
            } else if (activeTab === 'tickets') {
                // Загружаем билеты
                const ticketsData = await window.api.getAllTickets();
                setTickets(ticketsData || []);
            } else if (activeTab === 'users') {
                // Загружаем пользователей
                const usersData = await window.api.getAllUsers();
                setUsers(usersData || []);
            }
        } catch (error) {
            console.error('Error loading admin data:', error);
            setError('Ошибка загрузки данных: ' + error.message);
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

    const getRoleColor = (role) => {
        switch (role) {
            case 'admin': return 'bg-red-100 text-red-800';
            case 'manager': return 'bg-yellow-100 text-yellow-800';
            case 'customer': return 'bg-blue-100 text-blue-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const getRoleText = (role) => {
        switch (role) {
            case 'admin': return '👑 Администратор';
            case 'manager': return '👔 Менеджер';
            case 'customer': return '👤 Клиент';
            default: return role;
        }
    };

    if (user?.role !== 'admin') {
        return React.createElement('div', {
            className: 'fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm'
        },
            React.createElement('div', {
                className: 'bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 p-6 text-center'
            },
                React.createElement('div', {
                    className: 'text-6xl mb-4'
                }, '🚫'),
                React.createElement('h2', {
                    className: 'text-xl font-bold text-gray-900 mb-2'
                }, 'Доступ запрещен'),
                React.createElement('p', {
                    className: 'text-gray-600 mb-4'
                }, 'Только администраторы могут использовать эту панель'),
                React.createElement('button', {
                    className: 'bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors',
                    onClick: onClose
                }, 'Закрыть')
            )
        );
    }

    return React.createElement('div', {
        className: 'fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm'
    },
        React.createElement('div', {
            className: 'bg-white rounded-2xl shadow-2xl max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden'
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
                        }, '👑 Панель администратора'),
                        React.createElement('p', {
                            className: 'text-purple-200'
                        }, 'Управление системой Cinema Paradise')
                    ),
                    React.createElement('button', {
                        className: 'text-3xl hover:bg-white/20 w-10 h-10 rounded-full flex items-center justify-center transition-colors',
                        onClick: onClose
                    }, '×')
                )
            ),

            // Tabs
            React.createElement('div', {
                className: 'border-b border-gray-200'
            },
                React.createElement('div', {
                    className: 'flex space-x-1 p-1'
                },
                    React.createElement('button', {
                        className: `px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'stats' 
                                ? 'bg-purple-600 text-white' 
                                : 'text-gray-600 hover:bg-gray-100'
                        }`,
                        onClick: () => setActiveTab('stats')
                    }, '📊 Статистика'),
                    React.createElement('button', {
                        className: `px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'tickets' 
                                ? 'bg-purple-600 text-white' 
                                : 'text-gray-600 hover:bg-gray-100'
                        }`,
                        onClick: () => setActiveTab('tickets')
                    }, '🎫 Билеты'),
                    React.createElement('button', {
                        className: `px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'users' 
                                ? 'bg-purple-600 text-white' 
                                : 'text-gray-600 hover:bg-gray-100'
                        }`,
                        onClick: () => setActiveTab('users')
                    }, '👥 Пользователи'),
                    React.createElement('button', {
                        className: `px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'movies' 
                                ? 'bg-purple-600 text-white' 
                                : 'text-gray-600 hover:bg-gray-100'
                        }`,
                        onClick: () => setActiveTab('movies')
                    }, '🎬 Фильмы'),
                    React.createElement('button', {
                        className: `px-4 py-2 rounded-lg transition-colors ${
                            activeTab === 'sessions' 
                                ? 'bg-purple-600 text-white' 
                                : 'text-gray-600 hover:bg-gray-100'
                        }`,
                        onClick: () => setActiveTab('sessions')
                    }, '🎭 Сеансы')
                )
            ),

            // Content
            React.createElement('div', {
                className: 'p-6 overflow-y-auto max-h-[60vh]'
            },
                error && React.createElement('div', {
                    className: 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4'
                }, error),

                loading ? React.createElement('div', {
                    className: 'text-center py-8'
                },
                    React.createElement(window.LoadingSpinner),
                    React.createElement('p', {
                        className: 'text-gray-600 mt-2'
                    }, 'Загружаем данные...')
                ) : 
                
                // Stats Tab
                activeTab === 'stats' && stats ? React.createElement('div', null,
                    React.createElement('h3', {
                        className: 'text-lg font-semibold mb-4 text-gray-800'
                    }, '📊 Статистика системы'),
                    React.createElement('div', {
                        className: 'grid grid-cols-1 md:grid-cols-3 gap-6'
                    },
                        React.createElement('div', {
                            className: 'bg-blue-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '🎬'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-blue-600'
                            }, stats.movies),
                            React.createElement('p', {
                                className: 'text-blue-500'
                            }, 'Фильмов в каталоге')
                        ),
                        React.createElement('div', {
                            className: 'bg-green-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '🎭'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-green-600'
                            }, stats.sessions),
                            React.createElement('p', {
                                className: 'text-green-500'
                            }, 'Всего сеансов')
                        ),
                        React.createElement('div', {
                            className: 'bg-purple-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '🎫'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-purple-600'
                            }, stats.tickets),
                            React.createElement('p', {
                                className: 'text-purple-500'
                            }, 'Билетов продано')
                        ),
                        React.createElement('div', {
                            className: 'bg-yellow-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '👥'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-yellow-600'
                            }, stats.users),
                            React.createElement('p', {
                                className: 'text-yellow-500'
                            }, 'Пользователей')
                        ),
                        React.createElement('div', {
                            className: 'bg-orange-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '💰'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-orange-600'
                            }, `${stats.revenue} ₽`),
                            React.createElement('p', {
                                className: 'text-orange-500'
                            }, 'Общая выручка')
                        ),
                        React.createElement('div', {
                            className: 'bg-pink-50 rounded-lg p-6 text-center'
                        },
                            React.createElement('div', {
                                className: 'text-4xl mb-2'
                            }, '✅'),
                            React.createElement('h4', {
                                className: 'text-2xl font-bold text-pink-600'
                            }, stats.active_sessions),
                            React.createElement('p', {
                                className: 'text-pink-500'
                            }, 'Активных сеансов')
                        )
                    )
                ) :

                // Tickets Tab
                activeTab === 'tickets' ? React.createElement('div', null,
                    React.createElement('h3', {
                        className: 'text-lg font-semibold mb-4 text-gray-800'
                    }, '🎫 Все билеты'),
                    tickets.length === 0 ? React.createElement('div', {
                        className: 'text-center py-8'
                    },
                        React.createElement('div', {
                            className: 'text-6xl mb-4'
                        }, '🎫'),
                        React.createElement('p', {
                            className: 'text-gray-600'
                        }, 'Билетов пока нет')
                    ) : React.createElement('div', {
                        className: 'space-y-4'
                    },
                        tickets.map(ticket => 
                            React.createElement('div', {
                                key: ticket.id,
                                className: 'border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow'
                            },
                                React.createElement('div', {
                                    className: 'flex justify-between items-start mb-2'
                                },
                                    React.createElement('div', null,
                                        React.createElement('h4', {
                                            className: 'font-semibold text-gray-900'
                                        }, `Билет #${ticket.id}`),
                                        React.createElement('p', {
                                            className: 'text-gray-600'
                                        }, `Пользователь: ${ticket.user?.username || 'Неизвестно'}`)
                                    ),
                                    React.createElement('span', {
                                        className: `px-3 py-1 rounded-full text-sm font-medium ${
                                            ticket.is_confirmed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                        }`
                                    }, ticket.is_confirmed ? 'Подтвержден' : 'Ожидает')
                                ),
                                React.createElement('div', {
                                    className: 'grid grid-cols-1 md:grid-cols-4 gap-2 text-sm'
                                },
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, 'Фильм: '),
                                        React.createElement('span', null, ticket.session?.movie?.title || 'Неизвестно')
                                    ),
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, 'Место: '),
                                        React.createElement('span', null, `Ряд ${ticket.row_number}, Место ${ticket.seat_number}`)
                                    ),
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, 'Цена: '),
                                        React.createElement('span', {
                                            className: 'font-medium text-green-600'
                                        }, `${ticket.price} ₽`)
                                    ),
                                    React.createElement('div', null,
                                        React.createElement('span', {
                                            className: 'text-gray-600'
                                        }, 'Дата: '),
                                        React.createElement('span', null, formatDate(ticket.created_at))
                                    )
                                )
                            )
                        )
                    )
                ) :

                // Users Tab
                activeTab === 'users' ? React.createElement('div', null,
                    React.createElement('h3', {
                        className: 'text-lg font-semibold mb-4 text-gray-800'
                    }, '👥 Все пользователи'),
                    users.length === 0 ? React.createElement('div', {
                        className: 'text-center py-8'
                    },
                        React.createElement('div', {
                            className: 'text-6xl mb-4'
                        }, '👥'),
                        React.createElement('p', {
                            className: 'text-gray-600'
                        }, 'Пользователей пока нет')
                    ) : React.createElement('div', {
                        className: 'space-y-4'
                    },
                        users.map(userItem => 
                            React.createElement('div', {
                                key: userItem.id,
                                className: 'border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow'
                            },
                                React.createElement('div', {
                                    className: 'flex justify-between items-start mb-2'
                                },
                                    React.createElement('div', null,
                                        React.createElement('h4', {
                                            className: 'font-semibold text-gray-900'
                                        }, userItem.username),
                                        React.createElement('p', {
                                            className: 'text-gray-600'
                                        }, userItem.email)
                                    ),
                                    React.createElement('span', {
                                        className: `px-3 py-1 rounded-full text-sm font-medium ${getRoleColor(userItem.role)}`
                                    }, getRoleText(userItem.role))
                                ),
                                React.createElement('div', {
                                    className: 'text-sm text-gray-600'
                                },
                                    React.createElement('span', null, `Зарегистрирован: ${formatDate(userItem.created_at)}`)
                                )
                            )
                        )
                    )
                ) :

                // Movies & Sessions tabs (coming soon)
                (activeTab === 'movies' || activeTab === 'sessions') ? React.createElement('div', {
                    className: 'text-center py-8'
                },
                    React.createElement('div', {
                        className: 'text-6xl mb-4'
                    }, '🚧'),
                    React.createElement('h3', {
                        className: 'text-xl font-semibold text-gray-900 mb-2'
                    }, 'В разработке'),
                    React.createElement('p', {
                        className: 'text-gray-600'
                    }, `Управление ${activeTab === 'movies' ? 'фильмами' : 'сеансами'} будет добавлено в следующих версиях`)
                ) : null
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
                    }, 'Cinema Paradise Admin Panel v1.0'),
                    React.createElement('button', {
                        className: 'bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors',
                        onClick: onClose
                    }, 'Закрыть')
                )
            )
        )
    );
};

window.AdminPanel = AdminPanel; 