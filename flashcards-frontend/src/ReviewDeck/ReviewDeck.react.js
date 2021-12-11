import { useRecoilValue } from "recoil";
import { CurrentDeckCards } from "../atoms";
import { useState, useEffect } from "react";

export default function ReviewDeck() {
    const cards = useRecoilValue(CurrentDeckCards).data.cards;
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    
    if (cards == null) {
        return null;
    }

    return (
        <div className='container'>
            {<Card card={cards[currentCardIndex]} />}
            <button onClick={() => setCurrentCardIndex(currentCardIndex - 1)}>Previous</button>
            <button onClick={() => setCurrentCardIndex(currentCardIndex + 1)}>Next</button>
        </div>
    );
}

function Card({card}) {
    const [revealed, setRevealed] = useState(false);

    // hide answer when we change cards
    useEffect(() => {
        setRevealed(false)
    }, [card]);

    return (
        <div className='card' onClick={() => setRevealed(!revealed)}>
            <div>{card.question}</div>
            {revealed && <div>{card.answer}</div>}
        </div>
    );
}