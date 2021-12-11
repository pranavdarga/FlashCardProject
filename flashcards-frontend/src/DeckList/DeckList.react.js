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
    const [currentDeckName, setCurrentDeckName] = useState('');

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

    const isDeckSelected = currentDeckCards.length > 0 && currentDeckName.length > 0;
    console.log(isDeckSelected);
    console.log(currentDeckCards);
    console.log(currentDeckName)

    return (
        <div className='container'>
            <div>
                {deckList.map(deck => <div key={uuidv4()} className='deckEntry' onClick={async () => {
                    const response = await axios.get(`http://127.0.0.1:5000/deck_cards/${deck.deckid}`);
                    const cards = response.data.cards;
                    setCurrentDeckCards(cards);
                    setCurrentDeckName(deck.deckname);
                }}>{deck.deckname}</div>)}
            </div>
            <button onClick={() => {
                setPageNumber(PageNumbers.LOGIN);
                resetUserID();
            }}>Log out</button>
            <button onClick={() => setPageNumber(PageNumbers.NEW_DECK)}>Add new deck</button>
            <button onClick={() => setPageNumber(PageNumbers.REVIEW_DECK)} disabled={!isDeckSelected}>
                {isDeckSelected ? `Review ${currentDeckName}` : 'Select a deck to review'}
            </button>
            <button onClick={() => setPageNumber(PageNumbers.EDIT_DECK)} disabled={!isDeckSelected}>
                {isDeckSelected ? `Edit ${currentDeckName}` : 'Select a deck to edit'}
            </button>
        </div>
    )
}

async function getDeckList(userID) {
    const deckList = await axios.get(`http://127.0.0.1:5000/user_decks/${userID}`);
    return deckList.data.decks;
}