import { useRecoilValue } from "recoil";
import { CurrentDeckCards } from "../atoms";
import { useState } from "react";

export default function ReviewDeck() {
    const cards = useRecoilValue(CurrentDeckCards);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    
    if (cards == null) {
        return null;
    }

    console.log(cards[currentCardIndex]);

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

    return (
        <div className='card' onClick={setRevealed(true)}>
            <div>{card.question}</div>
            {revealed && <div>{card.answer}</div>}
        </div>
    );
}