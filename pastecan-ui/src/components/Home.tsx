import axios from 'axios';
import { h, createRef } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { route } from 'preact-router';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Container';
import ArchiveTable from './ArchiveTable';
import Paste from './Paste';
import PasteForm from './PasteForm';
import {
  languagesList,
  LanguageOption,
  MAX_PASTE_SIZE,
  exposureList,
} from '../common';
import getPastes from '../api';
import { GetPastesData } from '../types/response';

// eslint-disable-next-line react/no-unused-prop-types
const Home = (props: { path: string; loggedIn: boolean; }) => {
  const { loggedIn } = props;
  const [pastes, setPastes] = useState<GetPastesData[] | null>(null);
  const [alertMessage, setAlertMessage] = useState('');
  const [language, setLanguage] = useState<LanguageOption>('none');
  const [pasteContent, setPasteContent] = useState('New paste...\n');
  const [pasteExposure, setPasteExposure] = useState<'Public' | 'Private'>('Public');
  const [showAlert, setShowAlert] = useState(false);
  const [title, setTitle] = useState('');

  const languageRef = createRef();
  const exposureRef = createRef();

  useEffect(() => {
    const updatePastes = async () => {
      try {
        const result = await getPastes(0, 10);
        setPastes(result.data.items);
      } catch (error) {
        // fail silently
      }
    };

    updatePastes();
  }, []);

  const onLanguageChange = () => {
    setLanguage(languagesList[languageRef.current.options.selectedIndex]);
  };

  const onExposureChange = () => {
    setPasteExposure(exposureList[exposureRef.current.options.selectedIndex]);
  };

  const onCreate = async () => {
    if (pasteContent === '') {
      setAlertMessage('Cannot create an empty paste');
      setShowAlert(true);
    } else if (pasteContent.length > MAX_PASTE_SIZE) {
      setAlertMessage(`Paste exceeds maximum allowable size of ${MAX_PASTE_SIZE}`);
      setShowAlert(true);
    } else {
      setShowAlert(false);
      try {
        const response = await axios.post('/api/pastes', {
          content: pasteContent,
          exposure: pasteExposure,
          language,
          title,
        });
        route(`/pastes/${response.data.id}`);
      } catch (error) {
        setAlertMessage(`New paste creation did not succeed, sorry!\nError: ${error.message}`);
        setShowAlert(true);
      }
    }
  };

  return (
    <>
      <Container>
        <h1 className="d-flex justify-content-center pt-3">New Paste</h1>
        <Paste
          language={language}
          pasteContent={pasteContent}
          readOnly={false}
          onContentChange={setPasteContent}
        />
        <div className="pt-3">
          <Alert variant="danger" show={showAlert} onClose={() => setShowAlert(false)} dismissible>
            <p>{alertMessage}</p>
          </Alert>
        </div>
        <PasteForm
          onLanguageChange={onLanguageChange}
          onExposureChange={onExposureChange}
          onCreate={onCreate}
          setTitle={setTitle}
          exposureList={exposureList}
          loggedIn={loggedIn}
          languageRef={languageRef}
          exposureRef={exposureRef}
          defaultLanguage="none"
          defaultExposure="Public"
          defaultTitle=""
        />
        {(pastes !== null) && (
          <>
            <h1 className="d-flex justify-content-center pt-3">Recent Pastes</h1>
            <ArchiveTable data={pastes} showAuthor />
          </>
        )}
      </Container>
    </>
  );
};

export default Home;
