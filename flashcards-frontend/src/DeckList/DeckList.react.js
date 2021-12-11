import './DeckList.css'
import { useRecoilValue, useSetRecoilState, useResetRecoilState } from 'recoil';
import { UserIDAtom, PageNumberAtom, CurrentDeckCards } from '../atoms';
import PageNumbers from '../PageNumbers';
import axios from 'axios';
import { useEffect, useState } from 'react';
import {v4 as uuidv4} from 'uuid';

export default function DeckList() {
    const userID = useRecoilValue(UserIDAtom);
    const setPageNumber = useSetRecoilState(PageNumberAtom);
    const setCurrentDeckCards = useSetRecoilState(CurrentDeckCards);
    const resetuserID = useResetRecoilState(UserIDAtom);

    const [deckList, setDeckList] = useState([]);

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

    return (
        <div className='container'>
            <div>
                {deckList.map(deck => <div key={uuidv4()} className='deckEntry' onClick={async () => {
                    const cards = await axios.get('http://127.0.0.1:5000/decks/' + deck.deckid);
                    setCurrentDeckCards(cards);
                    setPageNumber(PageNumbers.REVIEW_DECK);
                }}>{deck.deckname}</div>)}
            </div>
            <button onClick={() => {
                setPageNumber(PageNumbers.LOGIN)
                resetuserID()
            }}>Log out</button>
            <button onClick={() => setPageNumber(PageNumbers.NEW_DECK)}>Add new deck</button>
        </div>
    )
}

async function getDeckList(userID) {
    const deckList = await axios.get(`http://127.0.0.1:5000/decks/${userID}`);
    return deckList.data.decks;
}