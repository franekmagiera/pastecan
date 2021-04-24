import axios from 'axios';
import { h, createRef } from 'preact';
import { route } from 'preact-router';
import { useEffect, useState } from 'preact/hooks';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Container';
import Paste from './Paste';
import PasteForm from './PasteForm';
import {
  LanguageOption,
  MAX_PASTE_SIZE,
  exposureList,
  languagesList,
} from '../common';

type PasteEditProps = {
  path: string; // eslint-disable-line react/no-unused-prop-types
  id: number;
  loggedIn: boolean;
  username: string;
};

const PasteEdit = (props: PasteEditProps) => {
  const [pasteLanguage, setPasteLanguage] = useState<LanguageOption>('none');
  const [pasteContent, setPasteContent] = useState('');
  const [pasteExposure, setPasteExposure] = useState<'Public' | 'Private'>('Public');
  const [pasteTitle, setPasteTitle] = useState('');
  const [pasteScreenName, setPasteScreenName] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');

  const languageRef = createRef();
  const exposureRef = createRef();

  useEffect(() => {
    const getPaste = async () => {
      setShowAlert(false);
      try {
        const response = await axios.get(`/api/pastes/${props.id}`);
        const {
          content,
          exposure,
          title,
          language,
          screenName,
        } = (response.data);
        setPasteContent(content);
        setPasteExposure(exposure);
        setPasteTitle(title);
        setPasteLanguage(language);
        setPasteScreenName(screenName);
      } catch (error) {
        setAlertMessage(`Could not fetch paste data, sorry!\nError: ${error.message}`);
        setShowAlert(true);
      }
    };

    getPaste();
  }, []);

  const onLanguageChange = () => {
    setPasteLanguage(languagesList[languageRef.current.options.selectedIndex]);
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
      try {
        await axios.put(`/api/pastes/${props.id}`, {
          content: pasteContent,
          exposure: pasteExposure,
          title: pasteTitle,
          language: pasteLanguage,
        });
        route(`/pastes/${props.id}`);
      } catch (error) {
        setAlertMessage(`Could not update paste, sorry!\nError: ${error.message}`);
        setShowAlert(true);
      }
    }
  };

  return (
    <Container>
      <div className="pt-3">
        <Alert
          variant="danger"
          show={showAlert}
          onClose={() => setShowAlert(false)}
          dismissible
        ><p>{alertMessage}</p>
        </Alert>
      </div>
      {props.loggedIn && (props.username === pasteScreenName)
        ? (
          <div className="pt-3">
            <h1 className="d-flex justify-content-center">Edit</h1>
            <Paste
              language={pasteLanguage}
              pasteContent={pasteContent}
              readOnly={false}
              onContentChange={setPasteContent}
            />
            <PasteForm
              onLanguageChange={onLanguageChange}
              onExposureChange={onExposureChange}
              onCreate={onCreate}
              setTitle={setPasteTitle}
              exposureList={exposureList}
              loggedIn={props.loggedIn}
              languageRef={languageRef}
              exposureRef={exposureRef}
              defaultLanguage={pasteLanguage}
              defaultExposure={pasteExposure}
              defaultTitle={pasteTitle}
            />
          </div>
        )
        : <Alert variant="danger" show dismissible>Could not verify user identity</Alert>}
    </Container>
  );
};

export default PasteEdit;
