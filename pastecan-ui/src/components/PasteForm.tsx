import { h, RefObject } from 'preact';
import { StateUpdater } from 'preact/hooks';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { LanguageOption, languagesList } from '../common';

type FormProps = {
    onLanguageChange: () => void;
    onExposureChange: () => void;
    onCreate: () => void;
    setTitle: StateUpdater<string>;
    exposureList: Readonly<('Public' | 'Private')[]>;
    loggedIn: boolean;
    languageRef: RefObject<HTMLSelectElement>;
    exposureRef: RefObject<HTMLSelectElement>;
    defaultLanguage: LanguageOption;
    defaultTitle: string;
    defaultExposure: 'Public' | 'Private';
};

const PasteForm = (props: FormProps) => {
  const handleKeyDown = (event: any) => {
    if (event.keyCode === 13) {
      event.preventDefault();
      props.onCreate();
    }
  };

  return (
    <Form className="pt-3">
      <Form.Group as={Row}>
        <Form.Label column sm={2}>Syntax highlighting</Form.Label>
        <Col sm={3}>
          <Form.Control as="select" onChange={props.onLanguageChange} defaultValue={[props.defaultLanguage]} ref={props.languageRef}>
            {languagesList.map((lang) => <option value={lang}>{lang}</option>)}
          </Form.Control>
        </Col>
      </Form.Group>
      <Form.Group as={Row}>
        <Form.Label column sm={2}>Paste title</Form.Label>
        <Col sm={3}>
          <Form.Control type="text" onChange={(event) => props.setTitle(event.target.value)} defaultValue={props.defaultTitle} onKeyDown={handleKeyDown} />
        </Col>
      </Form.Group>
      {props.loggedIn && (
        <Form.Group as={Row}>
          <Form.Label column sm={2}>Paste exposure</Form.Label>
          <Col sm={3}>
            <Form.Control as="select" onChange={props.onExposureChange} defaultValue={[props.defaultExposure]} ref={props.exposureRef}>
              {props.exposureList.map((value) => <option value={value}>{value}</option>)}
            </Form.Control>
          </Col>
        </Form.Group>
      )}
      <Form.Group as={Row}>
        <Col sm={{ span: 10, offset: 2 }}>
          <Button variant="primary" onClick={props.onCreate}>Send</Button>
        </Col>
      </Form.Group>
    </Form>
  );
};

export default PasteForm;
