import axios from 'axios';
import { h } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { Router, route } from 'preact-router';
import Cookies from 'js-cookie';
import Alert from 'react-bootstrap/Alert';
import Archive from './components/Archive';
import Header from './components/Header';
import Home from './components/Home';
import User from './components/User';
import PasteEdit from './components/PasteEdit';
import PasteReadOnly from './components/PasteReadOnly';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [showAlert, setShowAlert] = useState(false);

  const onLogout = async () => {
    try {
      await axios.get('/api/logout');
      Cookies.remove('screenName');
      setLoggedIn(false);
      setUsername('');
      window.location.reload();
      route('/');
    } catch (error) {
      setShowAlert(true);
    }
  };

  useEffect(() => {
    const screenName = Cookies.get('screenName');
    if (screenName) {
      setLoggedIn(true);
      setUsername(screenName);
    }
  }, []);

  return (
    <>
      <Header loggedIn={loggedIn} username={username} onLogout={onLogout} />
      <div className="pt-3">
        <Alert variant="danger" show={showAlert} onClose={() => setShowAlert(false)} dismissible>Error occured while logging out, please try again later</Alert>
      </div>
      <Router>
        <Home path="/" loggedIn={loggedIn} />
        <Archive path="/archive" />
        {/* @ts-expect-error */}
        <PasteReadOnly path="/pastes/:id" loggedIn={loggedIn} username={username} />
        {/* @ts-expect-error */}
        <PasteEdit path="/edit/:id" loggedIn={loggedIn} username={username} />
        {/* @ts-expect-error */}
        <User path="/users/:username" />
      </Router>
    </>
  );
};

export default App;
