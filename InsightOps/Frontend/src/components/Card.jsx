import PropTypes from 'prop-types';
import { memo } from 'react';
// import { BriefcaseIcon, FolderIcon, WrenchScrewdriverIcon } from '@heroicons/react/24/solid';

function Card({ title, number, icon, color }) {
  const IconComponent = icon;
  return (
    <div className="w-40 h-40 rounded-lg shadow-md bg-white hover:shadow-lg transition-shadow duration-200 flex flex-col items-center justify-center">
      {/* Icon Section */}
      <div className={`w-20 h-20 ${color} rounded flex items-center justify-center`}>
        <IconComponent className="w-10 h-10 text-white" />
      </div>
      {/* Content Section */}
      <div className="flex flex-col items-center mt-1">
        <h3 className="text-base font-semibold text-black">{title}</h3>
        <p className="text-sm text-black">{number}</p>
      </div>
    </div>
  );
}

Card.propTypes = {
  title: PropTypes.string.isRequired,
  number: PropTypes.number.isRequired,
  icon: PropTypes.elementType.isRequired,
  color: PropTypes.string.isRequired,
};

export default memo(Card);