import {atom} from 'recoil';
import PageNumbers from './PageNumbers'

export const PageNumberAtom = atom({
    key: 'PageNumber',
    default: PageNumbers.LOGIN
});

export const UserIDAtom = atom({
    key: 'UserIDAtom',
    default: ''
})

export const CurrentDeckCards = atom({
    key: 'CurrentDeckCards',
    default: []
})