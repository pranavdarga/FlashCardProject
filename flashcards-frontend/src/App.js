import './App.css';

import Login from './Login/Login.react'
import DeckList from './DeckList/DeckList.react'
import NewDeck from './NewDeck/NewDeck.react'
import ReviewDeck from './ReviewDeck/ReviewDeck.react'
import Analytics from './Analytics/Analytics.react'

import PageNumbers from './PageNumbers'
import { useRecoilValue } from 'recoil';

import {PageNumberAtom} from './atoms';

import Header from './Header';

function App() {
  const pages = [
    <Login key={PageNumbers.LOGIN} />,
    <DeckList userId='test' key={PageNumbers.DECK_LIST} />,
    <NewDeck userID='test' key={PageNumbers.NEW_DECK} />,
    <ReviewDeck key={PageNumbers.REVIEW_DECK} />,
    <Analytics />
  ];

  const currentPageNumber = useRecoilValue(PageNumberAtom);

  return (
    <div className="App">
      <Header />
      {pages[currentPageNumber]}
    </div>
  );
}

export default App;
