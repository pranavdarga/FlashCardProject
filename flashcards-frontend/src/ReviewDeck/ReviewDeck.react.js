import { useRecoilValue, useSetRecoilState } from "recoil";
import { CurrentDeckCards, PageNumberAtom, UserIDAtom } from "../atoms";
import { useState, useEffect } from "react";
import PageNumbers from "../PageNumbers";
import axios from "axios";

export default function ReviewDeck() {
    const cards = useRecoilValue(CurrentDeckCards);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const setPageNumber = useSetRecoilState(PageNumberAtom);
    const userid = useRecoilValue(UserIDAtom);

    if (cards == null) {
        return null;
    }

    return (
        <div className='container'>
            {<Card card={cards[currentCardIndex]} userid={userid} />}
            <button onClick={() => setCurrentCardIndex(currentCardIndex - 1)} disabled={currentCardIndex < 1}>Previous</button>
            <button onClick={() => 
                {
                    setCurrentCardIndex(currentCardIndex + 1)
                }} disabled={currentCardIndex + 1 >= cards.length}>Next</button>
            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}

function Card({card, userid}) {
    const [revealed, setRevealed] = useState(false);

    // hide answer when we change cards
    useEffect(() => {
        setRevealed(false)
    }, [card]);

    return (
        <div className='card' onClick={async () => {
            const date = new Date();
            console.log(getLocalISOString(date));

            const data = {
                cardid: card.cardid,
                time: getLocalISOString(date).slice(0, 19).replace('T', ' '),
                userid: userid
            };
            
            console.log('sending cardhistory')
            const response = await axios.post('https://flashcard-project-335103.uc.r.appspot.com//cardhistory', data);
            console.log(response);
            setRevealed(!revealed)
        }}>
            <div>{card.question}</div>
            {revealed && <div>{card.answer}</div>}
            {revealed && <div><i>{card.topic}</i></div>}

        </div>
    );
}

function getLocalISOString(date) {
    const offset = date.getTimezoneOffset()
    const offsetAbs = Math.abs(offset)
    const isoString = new Date(date.getTime() - offset * 60 * 1000).toISOString()
    return `${isoString.slice(0, -1)}${offset > 0 ? '-' : '+'}${String(Math.floor(offsetAbs / 60)).padStart(2, '0')}:${String(offsetAbs % 60).padStart(2, '0')}`
  }