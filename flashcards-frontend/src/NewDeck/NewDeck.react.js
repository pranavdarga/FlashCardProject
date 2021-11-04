import { useState, useCallback } from "react";

import './NewDeck.css';
import { useRecoilValue, useSetRecoilState } from "recoil";
import { UserIDAtom, PageNumberAtom } from "../atoms";
import { v4 as uuidv4 } from 'uuid';
import axios from "axios";

import PageNumbers from "../PageNumbers";

export default function NewDeck() {
    const userID = useRecoilValue(UserIDAtom);

    const [deckName, setDeckName] = useState('');
    const [cards, setCards] = useState([]);

    const [currentCardFront, setCurrentCardFront] = useState('');
    const [currentCardBack, setCurrentCardBack] = useState('');

    const setPageNumber = useSetRecoilState(PageNumberAtom);

    const updateTitle = useCallback((newValue) => {
        setDeckName(newValue);

        // API call to change deck here
    }, [setDeckName])

    const addNewCard = useCallback(() => {
        const cardsCopy = [...cards];
        cardsCopy.push({
            cardname: uuidv4(),
            question: currentCardFront,
            answer: currentCardBack
        });
        setCards(cardsCopy);

        // API call to change deck here
    }, [cards, currentCardBack, currentCardFront]);

    const saveDeck = useCallback(() => {
        const data = {
            deckname: deckName,
            userid: 10, // replace with actual user ID
            cards
        };

        console.log(data);
        axios.post('http://127.0.0.1:5000/createdeck', data);
        setPageNumber(PageNumbers.DECK_LIST);
    }, [cards, deckName, setPageNumber]);

    return (
        <div className='container'>
            <div className='inputContainer'>
                <input type='text' className='titleEntryBox' placeholder='Enter title here' onChange={e => updateTitle(e.target.value)} value={deckName} />
                <input type='text' className='newCardFront' placeholder='Enter question here' onChange={e => setCurrentCardFront(e.target.value)} value={currentCardFront} />
                <input type='text' className='newCardBack' placeholder='Enter answer here' onChange={e => setCurrentCardBack(e.target.value)} value={currentCardBack} />
                <button onClick={addNewCard}>Add new card</button>
            </div>
            <div className='existingCardsContainer'>
                {cards.map(card => (
                    <div className='card'>
                        <div className='cardFront'><strong>Front: </strong>{card.question}</div>
                        <div className='cardBack'><strong>Back: </strong>{card.answer}</div>
                    </div>
                ))}
            </div>
            <button onClick={saveDeck}>Save deck</button>
        </div>
    )
}