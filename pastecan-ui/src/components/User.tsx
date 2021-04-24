import { h } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Container';
import ArchiveTable from './ArchiveTable';
import getPastes from '../api';
import { GetPastesData } from '../types/response';

// eslint-disable-next-line react/no-unused-prop-types
const User = (props: { path: string, username: string }) => {
  const [pastes, setPastes] = useState<GetPastesData[] | null>(null);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');

  useEffect(() => {
    const updatePastes = async () => {
      try {
        setShowAlert(false);
        const result = await getPastes(offset, limit, props.username);
        setPastes(result.data.items);
      } catch (error) {
        setAlertMessage(`Could not fetch ${props.username}'s pastes, sorry!\nError: ${error.message}`);
        setShowAlert(true);
      }
    };

    updatePastes();
  }, []);

  return (
    <Container>
      <h1 className="d-flex justify-content-center pt-3">{props.username}</h1>
      <Alert className="pt-3" variant="danger" show={showAlert} onClose={() => setShowAlert(false)} dismissible>
        <p>{alertMessage}</p>
      </Alert>
      {(pastes !== null) && <ArchiveTable data={pastes} showAuthor={false} />}
    </Container>
  );
};

export default User;
