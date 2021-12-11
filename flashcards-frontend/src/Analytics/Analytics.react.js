import './Analytics.css'

import { useSetRecoilState } from "recoil";
import PageNumbers from "../PageNumbers";
import { PageNumberAtom } from '../atoms';

export default function Analytics() {
    const setPageNumber = useSetRecoilState(PageNumberAtom);

    return (
        <div className='container'>
            <div>Something special!</div>
            <button onClick={() => setPageNumber(PageNumbers.DECK_LIST)}>Return to home</button>
        </div>
    );
}