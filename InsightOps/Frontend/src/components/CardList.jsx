import PropTypes from 'prop-types';
import Card from './Card';

function CardList({ cards }) {
  return (
    <div className="flex justify-center gap-6 mt-4">
      {cards.map((card) => (
        <Card
          key={card.id}
          title={card.title}
          number={card.number}
          icon={card.icon}
          color={card.color}
        />
      ))}
    </div>
  );
}

CardList.propTypes = {
  cards: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      title: PropTypes.string.isRequired,
      number: PropTypes.number.isRequired,
      icon: PropTypes.elementType.isRequired,
      color: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default CardList;