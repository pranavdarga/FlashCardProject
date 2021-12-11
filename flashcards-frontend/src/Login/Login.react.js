import { useState } from "react";

import './Login.css'
import {PageNumberAtom, UserIDAtom} from '../atoms'
import PageNumbers from '../PageNumbers';
import { useSetRecoilState } from "recoil";
import axios from "axios";

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
            <button onClick={async () => {
                const data = {
                    username,
                    password
                };
        
                const response = await axios.post('http://127.0.0.1:5000/login', data);

                const status = response.data.status;

                if (status === "OK") {
                    const userid = response.data.userid;
                    setUserID(userid);
                    setPageNumber(PageNumbers.DECK_LIST);
                } else {
                    setPassword("");
                }
            }}>Login</button>
        </div>
    )
}