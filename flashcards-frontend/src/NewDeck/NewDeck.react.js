import { useState, useCallback } from "react";

import './NewDeck.css';
import { useRecoilValue, useSetRecoilState } from "recoil";
import { UserIDAtom, PageNumberAtom } from "../atoms";
import axios from "axios";

import PageNumbers from "../PageNumbers";

export default function NewDeck() {
    const userID = useRecoilValue(UserIDAtom);

    const [deckName, setDeckName] = useState('');
    const [cards, setCards] = useState([]);

    const [currentCardFront, setCurrentCardFront] = useState('');
    const [currentCardBack, setCurrentCardBack] = useState('');
    const [currentCardTopic, setCurrentCardTopic] = useState('');

    const [newDeckIDToImport, setNewDeckIDToImport] = useState('');

    const setPageNumber = useSetRecoilState(PageNumberAtom);

    const importDeckID = () => {
        // make API call with ID
        // console.log(newDeckIDToImport);
        const data = {
            deckid: newDeckIDToImport,
            userid: userID, // replace with actual user ID
        };

        axios.post('https://flashcard-project-335103.uc.r.appspot.com//importdeck', data);
    }

    const updateTitle = useCallback((newValue) => {
        setDeckName(newValue);
    }, [setDeckName])

    const addNewCard = useCallback(() => {
        const cardsCopy = [...cards];
        cardsCopy.push({
            question: currentCardFront,
            answer: currentCardBack,
            topic: currentCardTopic
        });
        setCards(cardsCopy);

        // API call to change deck here
    }, [cards, currentCardBack, currentCardFront, currentCardTopic]);

    const saveDeck = useCallback(async () => {
        const data = {
            deckname: deckName,
            userid: userID, // replace with actual user ID
            cards
        };

        await axios.post('https://flashcard-project-335103.uc.r.appspot.com//createdeck', data);
        setPageNumber(PageNumbers.DECK_LIST);
    }, [cards, deckName, setPageNumber, userID]);

    return (
        <div className='container'>
            <div className='inputContainer'>
                <input type='text' className='deckid_entry' placeholder='Enter existing deck ID here' onChange={e => setNewDeckIDToImport(e.target.value)} value={newDeckIDToImport} />
                <button onClick={importDeckID}>Import this deck ID</button>
                <br />
                <br />
                <input type='text' className='titleEntryBox' placeholder='Enter title of deck here' onChange={e => updateTitle(e.target.value)} value={deckName} />
                <input type='text' className='newCardFront' placeholder='Enter question here' onChange={e => setCurrentCardFront(e.target.value)} value={currentCardFront} />
                <input type='text' className='newCardBack' placeholder='Enter answer here' onChange={e => setCurrentCardBack(e.target.value)} value={currentCardBack} />
                <input type='text' className='newCardTopic' placeholder='Enter topic here (optional)' onChange={e => setCurrentCardTopic(e.target.value)} value={currentCardTopic} />

                <button onClick={addNewCard}>Add new card</button>
            </div>
            <div className='existingCardsContainer'>
                {cards.map(card => (
                    <div className='card'>
                        <div className='cardFront'><strong>Front: </strong>{card.question}</div>
                        <div className='cardBack'><strong>Back: </strong>{card.answer}</div>
                        <div className='cardTopic'><i>Topic: {card.topic}</i></div>
                    </div>
                ))}
            </div>
            <button onClick={saveDeck}>Save deck</button>
            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Go back</button>
        </div>
    )
}