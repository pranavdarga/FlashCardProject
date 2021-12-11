import { useState } from "react";

import './Login.css'
import {PageNumberAtom, UserIDAtom} from '../atoms'
import PageNumbers from '../PageNumbers';
import { useSetRecoilState } from "recoil";

export default function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const setUserID = useSetRecoilState(UserIDAtom);
    const setPageNumber = useSetRecoilState(PageNumberAtom);

    return (
        <div className='container'>
            <div>
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder='Enter username'/>
                <br />
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder='Enter password'/>
            </div>
            <button onClick={() => {
                const userid = 20; // fill in API function here to get user ID

                // replace this with "if credentials are valid below else clear password"
                setUserID(userid);
                setPageNumber(PageNumbers.DECK_LIST);
            }}>Login</button>
        </div>
    )
}