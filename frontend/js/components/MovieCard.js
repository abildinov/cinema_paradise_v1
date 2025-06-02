// Movie Card Component
const MovieCard = ({ movie, onSelect }) => {
    const [imageError, setImageError] = React.useState(false);

    const formatDuration = (minutes) => {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `${hours}ч ${mins}м`;
    };

    const formatRating = (rating) => {
        return rating ? rating.toFixed(1) : 'N/A';
    };

    return React.createElement('div', {
        className: 'bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-purple-500/20 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer',
        onClick: () => onSelect && onSelect(movie)
    },
        React.createElement('div', {
            className: 'relative h-64 bg-gray-700'
        },
            !imageError && movie.poster_url ? 
                React.createElement('img', {
                    src: movie.poster_url,
                    alt: movie.title,
                    className: 'w-full h-full object-cover',
                    onError: () => setImageError(true)
                }) :
                React.createElement('div', {
                    className: 'w-full h-full flex items-center justify-center text-gray-400'
                },
                    React.createElement('span', {
                        className: 'text-4xl'
                    }, '🎬')
                ),
            React.createElement('div', {
                className: 'absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-sm'
            }, `⭐ ${formatRating(movie.rating)}`)
        ),
        React.createElement('div', {
            className: 'p-4'
        },
            React.createElement('h3', {
                className: 'text-lg font-semibold text-white mb-2 line-clamp-2'
            }, movie.title),
            React.createElement('p', {
                className: 'text-gray-400 text-sm mb-2'
            }, movie.genre),
            React.createElement('p', {
                className: 'text-gray-500 text-sm mb-3'
            }, formatDuration(movie.duration)),
            movie.description && React.createElement('p', {
                className: 'text-gray-300 text-sm line-clamp-3'
            }, movie.description)
        )
    );
};

window.MovieCard = MovieCard;