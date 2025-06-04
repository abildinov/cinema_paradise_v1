// Login Modal Component
const LoginModal = ({ isOpen, onClose, onSuccess }) => {
    const [isLogin, setIsLogin] = React.useState(true);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState('');
    const [formData, setFormData] = React.useState({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            let response;
            if (isLogin) {
                response = await window.api.login(formData.username, formData.password);
            } else {
                response = await window.api.register({
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    first_name: formData.first_name,
                    last_name: formData.last_name
                });
            }
            
            if (onSuccess) {
                // Генерируем событие для обновления Header
                window.dispatchEvent(new CustomEvent('loginSuccess'));
                onSuccess(response.user || response);
            } else {
                // Генерируем событие для обновления Header
                window.dispatchEvent(new CustomEvent('loginSuccess'));
                onClose();
                window.location.reload();
            }
        } catch (err) {
            setError(err.message || 'Произошла ошибка');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    if (!isOpen) return null;

    return React.createElement('div', {
        className: 'fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4',
        onClick: (e) => e.target === e.currentTarget && onClose()
    },
        React.createElement('div', {
            className: 'bg-gray-800 rounded-lg p-6 w-full max-w-md'
        },
            React.createElement('div', {
                className: 'flex justify-between items-center mb-6'
            },
                React.createElement('h2', {
                    className: 'text-xl font-semibold text-white'
                }, isLogin ? 'Вход' : 'Регистрация'),
                React.createElement('button', {
                    className: 'text-gray-400 hover:text-white text-2xl',
                    onClick: onClose
                }, '×')
            ),

            error && React.createElement(window.Alert, {
                type: 'error',
                message: error,
                onClose: () => setError('')
            }),

            React.createElement('form', {
                onSubmit: handleSubmit,
                className: 'space-y-4'
            },
                React.createElement('div', null,
                    React.createElement('label', {
                        className: 'block text-sm font-medium text-gray-300 mb-1'
                    }, 'Имя пользователя'),
                    React.createElement('input', {
                        type: 'text',
                        required: true,
                        value: formData.username,
                        onChange: (e) => handleInputChange('username', e.target.value),
                        className: 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-purple-500 text-white'
                    })
                ),

                !isLogin && React.createElement(React.Fragment, null,
                    React.createElement('div', null,
                        React.createElement('label', {
                            className: 'block text-sm font-medium text-gray-300 mb-1'
                        }, 'Email'),
                        React.createElement('input', {
                            type: 'email',
                            required: true,
                            value: formData.email,
                            onChange: (e) => handleInputChange('email', e.target.value),
                            className: 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-purple-500 text-white'
                        })
                    ),
                    React.createElement('div', null,
                    React.createElement('label', {
                    className: 'block text-sm font-medium text-gray-300 mb-1'
                    }, 'Имя'),
                    React.createElement('input', {
                    type: 'text',
                    required: true,
                    value: formData.first_name,
                    onChange: (e) => handleInputChange('first_name', e.target.value),
                    className: 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-purple-500 text-white'
                    })
                    ),
                React.createElement('div', null,
                    React.createElement('label', {
                        className: 'block text-sm font-medium text-gray-300 mb-1'
                    }, 'Фамилия'),
                    React.createElement('input', {
                        type: 'text',
                        required: true,
                        value: formData.last_name,
                        onChange: (e) => handleInputChange('last_name', e.target.value),
                        className: 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-purple-500 text-white'
                    })
                )
                ),

                React.createElement('div', null,
                    React.createElement('label', {
                        className: 'block text-sm font-medium text-gray-300 mb-1'
                    }, 'Пароль'),
                    React.createElement('input', {
                        type: 'password',
                        required: true,
                        value: formData.password,
                        onChange: (e) => handleInputChange('password', e.target.value),
                        className: 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-purple-500 text-white'
                    })
                ),

                React.createElement('button', {
                    type: 'submit',
                    disabled: loading,
                    className: 'w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center'
                },
                    loading ? React.createElement(window.LoadingSpinner, { size: 'small' }) : (isLogin ? 'Войти' : 'Зарегистрироваться')
                )
            ),

            React.createElement('div', {
                className: 'text-center mt-4'
            },
                React.createElement('button', {
                    type: 'button',
                    onClick: () => setIsLogin(!isLogin),
                    className: 'text-purple-400 hover:text-purple-300 text-sm'
                }, isLogin ? 'Нет аккаунта? Зарегистрируйтесь' : 'Уже есть аккаунт? Войдите')
            )
        )
    );
};

// Глобальная функция для открытия модального окна
window.showLoginModal = () => {
    const event = new CustomEvent('openLoginModal');
    window.dispatchEvent(event);
};

window.LoginModal = LoginModal;