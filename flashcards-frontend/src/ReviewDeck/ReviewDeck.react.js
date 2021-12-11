import { useRecoilValue, useSetRecoilState } from "recoil";
import { CurrentDeckCards, PageNumberAtom, UserIDAtom } from "../atoms";
import { useState, useEffect } from "react";
import PageNumbers from "../PageNumbers";
import axios from "axios";

export default function ReviewDeck() {
    const cards = useRecoilValue(CurrentDeckCards);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const setPageNumber = useSetRecoilState(PageNumberAtom);

    if (cards == null) {
        return null;
    }

    return (
        <div className='container'>
            {<Card card={cards[currentCardIndex]} />}
            <button onClick={() => setCurrentCardIndex(currentCardIndex - 1)} disabled={currentCardIndex < 1}>Previous</button>
            <button onClick={() => setCurrentCardIndex(currentCardIndex + 1)} disabled={currentCardIndex + 1 >= cards.length}>Next</button>
            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}

function Card({card}) {
    const userid = useRecoilValue(UserIDAtom);
    const [revealed, setRevealed] = useState(false);

    // hide answer when we change cards
    useEffect(() => {
        setRevealed(false)
    }, [card]);

    return (
        <div className='card' onClick={async () => {
            const time = Date.getTime();
            const data = {
                cardid: card.cardid,
                time: time,
                userid: userid
            };
            
            const response = await axios.post('http://127.0.0.1:5000/cardhistory', data);
            const status = response.data.status;
            
            if (status=='OK') {
                setRevealed(!revealed)
            }
            else {
                console.log("Error adding to cardhistory");
            }
        }}>
            <div>{card.question}</div>
            {revealed && <div>{card.answer}</div>}
        </div>
    );
}