import PropTypes from 'prop-types';
// import { memo } from 'react';

function Card({ title, number, icon, color, path, onCardClick }) {
  const IconComponent = icon;
  const baseClasses = 'w-48 h-48 rounded-lg shadow-md bg-white flex flex-col items-center justify-center p-4';
  const transitionClasses = 'transition-all duration-300 ease-in-out';
  const clickableStyles = path 
    ? `
        cursor-pointer
        hover:scale-65
        hover:-translate-y-1
        hover:ring-4
        hover:ring-[#111827]
      ` 
    : 'cursor-default';

  return (
    <div className={`${baseClasses} ${transitionClasses} ${clickableStyles}`}
      onClick={() => {
        if (onCardClick && path) {
          onCardClick(path);
        }
      }}
    >
      {/* Icon Section */}
      <div className={`w-20 h-20 ${color} rounded-full flex items-center justify-center`}>
        <IconComponent className="w-10 h-10 text-[#F9FAFB]" />
      </div>
      {/* Content Section */}
      <div className="flex flex-col items-center mt-1 text-center">
        <h3 className="text-base font-semibold text-[#1F2937]">{title}</h3>
        <p className="text-sm text-black">{number}</p>
      </div>
    </div>
  );
}

Card.propTypes = {
  title: PropTypes.string.isRequired,
  number: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.elementType.isRequired,
  color: PropTypes.string.isRequired,
  path: PropTypes.string,
  onCardClick: PropTypes.func,
};

Card.defaultProps = {
  path: null,
  onCardClick: () => {},
};

export default Card;