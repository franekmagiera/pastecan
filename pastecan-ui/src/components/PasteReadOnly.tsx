import axios from 'axios';
import { h } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { route } from 'preact-router';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import Paste from './Paste';
import { GetPasteData } from '../types/response';

type PasteReadOnlyProps = {
  path: string; // eslint-disable-line react/no-unused-prop-types
  id: number;
  loggedIn: boolean;
  username: string;
}

const PasteReadOnly = (props: PasteReadOnlyProps) => {
  const [pasteData, setPasteData] = useState<GetPasteData | null>(null);
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [alertVariant, setAlertVariant] = useState('');

  useEffect(() => {
    const getPaste = async () => {
      setShowAlert(false);
      try {
        const response = await axios.get(`/api/pastes/${props.id}`);
        setPasteData(response.data);
      } catch (error) {
        setAlertMessage(`Could not fetch paste data, sorry!\nError: ${error.message}`);
        setAlertVariant('danger');
        setShowAlert(true);
      }
    };

    getPaste();
  }, []);

  const onDelete = async () => {
    setShowAlert(false);
    try {
      await axios.delete(`/api/pastes/${props.id}`);
      // API returns only 204 on success.
      setAlertMessage('Paste deleted! Redirecting to Home in 2s...');
      setAlertVariant('info');
      setShowAlert(true);
      setTimeout(() => { route('/'); }, 2000);
    } catch (error) {
      setAlertMessage(`Could not delete the paste, sorry!\nError: ${error.message}`);
      setAlertVariant('danger');
      setShowAlert(true);
    }
  };

  return (
    <Container>
      <div className="pt-3">
        <Alert
          variant={alertVariant}
          show={showAlert}
          onClose={() => setShowAlert(false)}
          dismissible
        >
          <p>{alertMessage}</p>
        </Alert>
      </div>
      {pasteData ? (
        <>
          <h1 className="d-flex justify-content-center pt-3">{pasteData.title}</h1>
          <Row>
            <Col>Created by: {pasteData.screenName ? <a href={`/users/${pasteData.screenName}`}>{pasteData.screenName}</a> : 'Guest'}</Col>
          </Row>
          <Row>
            <Col>On: {pasteData.date}</Col>
          </Row>
          <Paste language={pasteData.language} pasteContent={pasteData.content} readOnly />
          {props.loggedIn && (props.username === pasteData.screenName) ? (
            <Form className="pt-3">
              <Form.Group as={Row}>
                <Col>
                  <Button variant="secondary" onClick={() => route(`/edit/${props.id}`)}>Edit</Button>{' '}
                  <Button variant="danger" onClick={onDelete}>Delete</Button>
                </Col>
              </Form.Group>
            </Form>
          ) : <></>}
        </>
      ) : <></>}
    </Container>
  );
};

export default PasteReadOnly;
