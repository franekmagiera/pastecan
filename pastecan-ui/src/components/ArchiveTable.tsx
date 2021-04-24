import { h } from 'preact';
import Table from 'react-bootstrap/Table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import { GetPastesData } from '../types/response';

const ArchiveTable = (props: { data: GetPastesData[], showAuthor: boolean }) => (
  <Table striped bordered hover>
    <thead>
      <tr>
        <th>Title</th>
        <th>Created</th>
        <th>Language</th>
        {props.showAuthor ? <th>Author</th> : ''}
      </tr>
    </thead>
    <tbody>
      {props.data.map((entry) => (
        <tr>
          <td>{(entry.exposure === 'Private') ? <FontAwesomeIcon icon={faLock} /> : ''}<a href={`/pastes/${entry.id}`}> {entry.title}</a></td>
          <td>{entry.date}</td>
          <td>{entry.language}</td>
          {props.showAuthor ? <td>{entry.screenName ? <a href={`/users/${entry.screenName}`}>{entry.screenName}</a> : 'Guest'}</td> : ''}
        </tr>
      ))}
    </tbody>
  </Table>
);

export default ArchiveTable;
