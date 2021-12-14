import './Analytics.css'

import { useRecoilValue, useSetRecoilState } from "recoil";
import PageNumbers from "../PageNumbers";
import { PageNumberAtom, UserIDAtom } from '../atoms';
import axios from "axios";
import { useEffect, useState } from 'react';

export default function Analytics() {
    const setPageNumber = useSetRecoilState(PageNumberAtom);
    const userid = useRecoilValue(UserIDAtom);

    const [results, setResults] = useState({
        most_deck: {deckname: ''},
        least_deck: {deckname: ''}
    });

    useEffect(() => {
        async function getNumbers(userid) {
            const data = {userid: userid};
            console.log(data);
            const response = await axios.get(`http://127.0.0.1:5000/analytics/${userid}`);
            console.log(response);
            setResults(response.data);
        }

        getNumbers(userid);
    }, [userid]);

    return (
        <div className='container'>
            <div>Your most used deck is: {results.most_deck.deckname}</div>
            <div>Your least used deck is: {results.least_deck.deckname}</div>

            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}
