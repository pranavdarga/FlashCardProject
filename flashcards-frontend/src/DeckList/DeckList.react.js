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
    const [currentDeckName, setCurrentDeckName] = useState([]);


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
    }, []);

    return (
        <div className='container'>
            <div>
                {deckList.map(deck => <div key={uuidv4()} className='deckEntry' onClick={async () => {
                    console.log(deck.deckid)
                    const cards = await axios.get('http://127.0.0.1:5000/decks/' + deck.deckid);
                    console.log(cards);
                    setCurrentDeckCards(cards);
                    setCurrentDeckName(deck.deckname);
                    // setPageNumber(PageNumbers.REVIEW_DECK)
                }}>{deck.deckname}</div>)}
            </div>
            <button onClick={() => {
                setPageNumber(PageNumbers.LOGIN)
                resetuserID()
            }}>Log out</button>
            <button onClick={() => setPageNumber(PageNumbers.NEW_DECK)}>Add new deck</button>
        <button onClick={() => setPageNumber(PageNumbers.REVIEW_DECK)}>Review {currentDeckName}</button>
        </div>
    )
}

async function getDeckList(userID) {
    const deckList = await axios.get('http://127.0.0.1:5000/decks');
    return deckList.data.decks;
}