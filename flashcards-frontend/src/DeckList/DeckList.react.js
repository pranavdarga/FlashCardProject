import './DeckList.css'
import { useRecoilValue, useSetRecoilState, useResetRecoilState, useRecoilState } from 'recoil';
import { UserIDAtom, PageNumberAtom, CurrentDeckCards } from '../atoms';
import PageNumbers from '../PageNumbers';
import axios from 'axios';
import { useEffect, useState } from 'react';
import {v4 as uuidv4} from 'uuid';

export default function DeckList() {
    const userID = useRecoilValue(UserIDAtom);
    const setPageNumber = useSetRecoilState(PageNumberAtom);
    const [currentDeckCards, setCurrentDeckCards] = useRecoilState(CurrentDeckCards);
    const resetUserID = useResetRecoilState(UserIDAtom);

    const [deckList, setDeckList] = useState([]);
    const [currentDeck, setCurrentDeck] = useState({
        deckname: '',
        deckid: 0
    });

    useEffect(() => {
        async function updateDeckList() {
            const newDeckList = await getDeckList(userID);
            setDeckList(newDeckList);
        }

        updateDeckList();
    }, [userID]);

    useEffect(() => {
        async function updateDeckList() {
            const newDeckList = await getDeckList(userID);
            setDeckList(newDeckList);
        }

        updateDeckList();
    }, [userID]);

    const isDeckSelected = currentDeckCards.length > 0 && currentDeck.deckname.length > 0;

    return (
        <div className='container'>
            <div>
                {deckList.map(deck => <div key={uuidv4()} className='deckEntry' onClick={async () => {
                    const response = await axios.get(`http://127.0.0.1:5000/deck_cards/${deck.deckid}`);
                    const cards = response.data.cards;
                    setCurrentDeckCards(cards);
                    setCurrentDeck(deck);
                }}>{deck.deckname} ({deck.num_cards} cards, last reviewed {deck.last_reviewed_string})</div>)}
            </div>
            <button onClick={() => {
                setPageNumber(PageNumbers.LOGIN);
                resetUserID();
            }}>Log out</button>
            <button onClick={() => setPageNumber(PageNumbers.NEW_DECK)}>Add new deck</button>
            <button onClick={() => setPageNumber(PageNumbers.REVIEW_DECK)} disabled={!isDeckSelected}>
                {isDeckSelected ? `Review ${currentDeck.deckname}` : 'Select a deck to review'}
            </button>
            <button onClick={() => setPageNumber(PageNumbers.ANALYTICS)}>Explore your analytics</button>
        {currentDeck.deckid > 0 && <div>Current deck ID: {currentDeck.deckid}</div>}
        </div>
    )
}

async function getDeckList(userID) {
    const deckList = await axios.get(`http://127.0.0.1:5000/user_decks/${userID}`);
    console.log('keke');
    console.log(deckList);
    return deckList.data.decks;
}