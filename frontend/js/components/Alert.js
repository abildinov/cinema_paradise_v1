// Alert Component
const Alert = ({ type = 'info', message, onClose }) => {
    const typeClasses = {
        success: 'bg-green-100 border-green-500 text-green-700',
        error: 'bg-red-100 border-red-500 text-red-700',
        warning: 'bg-yellow-100 border-yellow-500 text-yellow-700',
        info: 'bg-blue-100 border-blue-500 text-blue-700'
    };

    React.useEffect(() => {
        if (type !== 'error') {
            const timer = setTimeout(() => {
                onClose && onClose();
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [type, onClose]);

    return React.createElement('div', {
        className: 'fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm',
        style: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0 }
    },
        React.createElement('div', {
            className: `max-w-md w-full mx-4 border-l-4 p-6 shadow-xl rounded-lg ${typeClasses[type]} relative animate-bounce`
        },
            React.createElement('p', {
                className: 'font-medium text-lg'
            }, message),
            onClose && React.createElement('button', {
                className: 'absolute top-2 right-2 text-xl font-bold opacity-70 hover:opacity-100 focus:outline-none',
                onClick: onClose
            }, '×')
        )
    );
};

window.Alert = Alert;