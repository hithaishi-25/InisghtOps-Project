import PropTypes from 'prop-types';
import Card from './Card';

function CardList({ cards, onCardClick }) {
  return (
    <div className="flex justify-center gap-7 mt-9">
      {cards.map((card) => (
        <Card
          key={card.id}
          title={card.title}
          number={card.number}
          icon={card.icon}
          color={card.color}
          path={card.path}
          onCardClick={onCardClick}
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
      path: PropTypes.string,
    })
  ).isRequired,
  onCardClick: PropTypes.func,
};

CardList.defaultProps = {
    onCardClick: () => {},
};

export default CardList;