// Booking Modal Component
const BookingModal = ({ isOpen, session, onClose, onSuccess }) => {
    console.log('BookingModal: Component called with props:', {
        isOpen: isOpen,
        session: session,
        hasSession: !!session,
        sessionId: session?.id,
        sessionTitle: session?.movie?.title,
        propsType: typeof isOpen,
        sessionType: typeof session
    });
    
    console.log('BookingModal: Rendering with props:', {
        isOpen,
        hasSession: !!session,
        sessionId: session?.id,
        sessionTitle: session?.movie?.title
    });
    
    const [selectedSeats, setSelectedSeats] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState('');
    const [seatMap, setSeatMap] = React.useState([]);

    React.useEffect(() => {
        console.log('BookingModal: useEffect triggered', { isOpen, hasSession: !!session });
        if (isOpen && session) {
            generateSeatMap();
        }
    }, [isOpen, session]);

    const generateSeatMap = () => {
        if (!session.hall) {
            console.log('BookingModal: No hall data', session);
            return;
        }
        
        console.log('BookingModal: Generating seat map for hall:', session.hall);
        
        const totalSeats = session.hall.capacity || session.hall.total_seats || 100;
        const rows = session.hall.rows || Math.ceil(totalSeats / 10);
        const seatsPerRow = session.hall.seats_per_row || Math.ceil(totalSeats / rows);
        
        console.log('BookingModal: Hall config:', { totalSeats, rows, seatsPerRow });
        
        const map = [];
        
        for (let row = 0; row < rows; row++) {
            const rowSeats = [];
            for (let seat = 0; seat < seatsPerRow; seat++) {
                const seatNumber = row * seatsPerRow + seat + 1;
                if (seatNumber <= totalSeats) {
                    rowSeats.push({
                        number: seatNumber,
                        row: row + 1,
                        seat: seat + 1,
                        isBooked: Math.random() < 0.3 // Случайно занятые места
                    });
                }
            }
            if (rowSeats.length > 0) {
                map.push(rowSeats);
            }
        }
        
        console.log('BookingModal: Generated seat map:', map);
        setSeatMap(map);
    };

    const handleSeatClick = (seatNumber) => {
        setSelectedSeats(prev => {
            if (prev.includes(seatNumber)) {
                return prev.filter(s => s !== seatNumber);
            } else {
                return [...prev, seatNumber];
            }
        });
    };

    const handleBooking = async () => {
        if (selectedSeats.length === 0) {
            setError('Выберите хотя бы одно место');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const booking = await window.api.createTicket({
                session_id: session.id,
                seat_numbers: selectedSeats,
                total_price: selectedSeats.length * session.price
            });
            
            onSuccess && onSuccess(booking);
            onClose();
        } catch (err) {
            setError(err.message || 'Ошибка при бронировании');
        } finally {
            setLoading(false);
        }
    };

    const totalPrice = selectedSeats.length * (session?.price || 0);

    console.log('BookingModal: Before render check:', {
        isOpen,
        hasSession: !!session,
        willRender: !(!isOpen || !session),
        isOpenType: typeof isOpen,
        isOpenValue: isOpen,
        sessionExists: session !== null && session !== undefined
    });

    if (!isOpen || !session) {
        console.log('BookingModal: Returning null because isOpen:', isOpen, 'session:', !!session);
        return null;
    }

    console.log('BookingModal: About to render modal DOM element');

    return React.createElement('div', {
        className: 'fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4',
        onClick: (e) => e.target === e.currentTarget && onClose()
    },
        React.createElement('div', {
            className: 'bg-gray-800 rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto'
        },
            React.createElement('div', {
                className: 'flex justify-between items-center mb-6'
            },
                React.createElement('div', null,
                    React.createElement('h2', {
                        className: 'text-xl font-semibold text-white'
                    }, 'Выбор мест'),
                    React.createElement('p', {
                        className: 'text-gray-400 text-sm'
                    }, `${session.movie?.title} - ${session.hall?.name}`)
                ),
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

            // Экран
            React.createElement('div', {
                className: 'mb-6'
            },
                React.createElement('div', {
                    className: 'bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full mb-2'
                }),
                React.createElement('p', {
                    className: 'text-center text-gray-400 text-sm'
                }, 'ЭКРАН')
            ),

            // Схема мест
            React.createElement('div', {
                className: 'mb-6'
            },
                seatMap.map((row, rowIndex) =>
                    React.createElement('div', {
                        key: rowIndex,
                        className: 'flex justify-center items-center mb-2'
                    },
                        React.createElement('span', {
                            className: 'text-gray-400 text-sm w-6 text-center mr-2'
                        }, rowIndex + 1),
                        ...row.map(seat =>
                            React.createElement('button', {
                                key: seat.number,
                                className: `w-8 h-8 mx-1 rounded text-xs font-medium transition-colors ${
                                    seat.isBooked 
                                        ? 'bg-red-600 text-white cursor-not-allowed' 
                                        : selectedSeats.includes(seat.number)
                                            ? 'bg-purple-600 text-white'
                                            : 'bg-gray-600 text-gray-300 hover:bg-gray-500'
                                }`,
                                onClick: () => !seat.isBooked && handleSeatClick(seat.number),
                                disabled: seat.isBooked
                            }, seat.number)
                        )
                    )
                )
            ),

            // Легенда
            React.createElement('div', {
                className: 'flex justify-center space-x-6 mb-6 text-sm'
            },
                React.createElement('div', {
                    className: 'flex items-center'
                },
                    React.createElement('div', {
                        className: 'w-4 h-4 bg-gray-600 rounded mr-2'
                    }),
                    React.createElement('span', {
                        className: 'text-gray-400'
                    }, 'Свободно')
                ),
                React.createElement('div', {
                    className: 'flex items-center'
                },
                    React.createElement('div', {
                        className: 'w-4 h-4 bg-purple-600 rounded mr-2'
                    }),
                    React.createElement('span', {
                        className: 'text-gray-400'
                    }, 'Выбрано')
                ),
                React.createElement('div', {
                    className: 'flex items-center'
                },
                    React.createElement('div', {
                        className: 'w-4 h-4 bg-red-600 rounded mr-2'
                    }),
                    React.createElement('span', {
                        className: 'text-gray-400'
                    }, 'Занято')
                )
            ),

            // Итого и кнопка
            React.createElement('div', {
                className: 'flex justify-between items-center'
            },
                React.createElement('div', null,
                    React.createElement('p', {
                        className: 'text-white'
                    }, `Выбрано мест: ${selectedSeats.length}`),
                    React.createElement('p', {
                        className: 'text-purple-400 font-semibold text-lg'
                    }, `Итого: ${totalPrice} ₽`)
                ),
                React.createElement('button', {
                    onClick: handleBooking,
                    disabled: loading || selectedSeats.length === 0,
                    className: 'bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center'
                },
                    loading ? React.createElement(window.LoadingSpinner, { size: 'small' }) : 'Забронировать'
                )
            )
        )
    );
};

window.BookingModal = BookingModal;