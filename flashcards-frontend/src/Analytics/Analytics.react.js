import './Analytics.css'

import { useRecoilValue, useSetRecoilState } from "recoil";
import PageNumbers from "../PageNumbers";
import { PageNumberAtom, UserIDAtom } from '../atoms';
import axios from "axios";

export default function Analytics() {
    const setPageNumber = useSetRecoilState(PageNumberAtom);
    const userid = useRecoilValue(UserIDAtom);
    
    var results = getNumbers(userid);

    return (
        <div className='container'>
            <div>{}'s top card is: {}</div>
            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}
async function getNumbers(userid) {
    const data = {userid: userid};
    const response = await axios.get('https://flashcard-project-335103.uc.r.appspot.com/analytics', data);
    return 0;
}