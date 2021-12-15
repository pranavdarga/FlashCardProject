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
        least_deck: {deckname: ''},
        card_table: []
    });

    useEffect(() => {
        async function getNumbers(userid) {
            const response = await axios.get(`http://127.0.0.1:5000/user_stats/${userid}`);
            setResults(response.data);
        }

        getNumbers(userid);
    }, [userid]);

    return (
        <div className='container'>
            <div>Your most reviewed deck is: {results.most_deck.deckname}</div>
            <div>Your least reviewed deck is: {results.least_deck.deckname}</div>

            <br />

            {results.card_table.map((entry, index) => {
                console.log(entry);

                // query returned nothing
                if (entry[1].length === 0) {
                    return null;
                }

                return (
                    <div key={index}>
                        <div>The least reviewed card for {entry[0]} was: </div>
                        <div><strong>Question: </strong> {entry[1][0][0]}</div>
                        <div><strong>Answer: </strong> {entry[1][0][1]}</div>
                        <div><i>Topic: {entry[1][0][2]}</i></div>
                        <br />
                        <div>The most reviewed card for {entry[0]} was: </div>
                        <div><strong>Question: </strong> {entry[2][0][0]}</div>
                        <div><strong>Answer: </strong> {entry[2][0][1]}</div>
                        <div><i>Topic: {entry[2][0][2]}</i></div>
                        <br />
                        <br />
                    </div>
                );
            })}

            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}
