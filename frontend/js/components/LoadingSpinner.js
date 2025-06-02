// Loading Spinner Component
const LoadingSpinner = ({ size = 'medium' }) => {
    const sizeClasses = {
        small: 'w-4 h-4',
        medium: 'w-8 h-8',
        large: 'w-12 h-12'
    };

    return React.createElement('div', {
        className: 'flex justify-center items-center'
    },
        React.createElement('div', {
            className: `${sizeClasses[size]} animate-spin rounded-full border-2 border-gray-300 border-t-purple-600`
        })
    );
};

window.LoadingSpinner = LoadingSpinner;