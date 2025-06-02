// Session Card Component
const SessionCard = ({ session, onBook }) => {
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const formatPrice = (price) => {
        return `${price} ₽`;
    };

    const getAvailableSeats = () => {
        // Убеждаемся что available_seats - это число
        let availableSeats = session.available_seats;
        
        // Преобразуем в число если это строка
        if (typeof availableSeats === 'string') {
            availableSeats = parseInt(availableSeats, 10);
        }
        
        // Возвращаем 0 если не число или NaN
        return (typeof availableSeats === 'number' && !isNaN(availableSeats)) ? availableSeats : 0;
    };

    const getTotalSeats = () => {
        // Убеждаемся что capacity - это число
        let capacity = session.hall?.capacity;
        
        // Преобразуем в число если это строка
        if (typeof capacity === 'string') {
            capacity = parseInt(capacity, 10);
        }
        
        // Возвращаем 0 если не число или NaN
        return (typeof capacity === 'number' && !isNaN(capacity)) ? capacity : 0;
    };

    const availableSeats = getAvailableSeats();
    const totalSeats = getTotalSeats();
    const isAvailable = availableSeats > 0;

    return React.createElement('div', {
        className: `bg-gray-800 rounded-lg p-4 border ${isAvailable ? 'border-gray-700 hover:border-purple-500' : 'border-red-500/50'} transition-colors`
    },
        React.createElement('div', {
            className: 'flex justify-between items-start mb-3'
        },
            React.createElement('div', null,
                React.createElement('h3', {
                    className: 'text-lg font-semibold text-white mb-1'
                }, session.movie?.title || 'Фильм'),
                React.createElement('p', {
                    className: 'text-gray-400 text-sm'
                }, session.hall?.name || 'Зал')
            ),
            React.createElement('div', {
                className: 'text-right'
            },
                React.createElement('p', {
                    className: 'text-purple-400 font-semibold'
                }, formatPrice(session.price)),
                React.createElement('p', {
                    className: 'text-gray-500 text-sm'
                }, formatDate(session.start_time))
            )
        ),
        React.createElement('div', {
            className: 'flex justify-between items-center'
        },
            React.createElement('div', {
                className: 'flex items-center space-x-4'
            },
                React.createElement('span', {
                    className: `text-sm ${isAvailable ? 'text-green-400' : 'text-red-400'}`
                }, `${availableSeats} свободных мест`),
                React.createElement('span', {
                    className: 'text-gray-400 text-sm'
                }, `Всего: ${totalSeats}`)
            ),
            React.createElement('button', {
                className: `px-4 py-2 rounded transition-colors ${
                    isAvailable 
                        ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                        : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                }`,
                onClick: () => {
                    console.log('SessionCard: Button clicked!', {
                        isAvailable,
                        hasOnBook: !!onBook,
                        session: session.id
                    });
                    
                    if (isAvailable && onBook) {
                        console.log('SessionCard: Calling onBook with session:', session);
                        onBook(session);
                    } else {
                        console.log('SessionCard: Cannot book - isAvailable:', isAvailable, 'onBook:', !!onBook);
                    }
                },
                disabled: !isAvailable
            }, isAvailable ? 'Забронировать' : 'Нет мест')
        )
    );
};

window.SessionCard = SessionCard;