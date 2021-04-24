import axios from 'axios';
import { h } from 'preact';
import { route } from 'preact-router';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter } from '@fortawesome/free-brands-svg-icons';

type HeaderProps = {
  loggedIn: boolean;
  username: string;
  onLogout: () => void;
};

const Header = (props: HeaderProps) => {
  const { loggedIn, username, onLogout } = props;

  const login = async (name: string) => {
    try {
      await axios.get(`/api/${name}_login`);
      window.location.reload();
      route('/');
    } catch (error) {
      // fail silently
    }
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand>Pastecan</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/archive">Archive</Nav.Link>
            <NavDropdown title="Mock login" id="mock-login-dropdown">
              <NavDropdown.Item onClick={() => login('jane')}>Log in as Jane</NavDropdown.Item>
              <NavDropdown.Item onClick={() => login('john')}>Log in as John</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            {loggedIn
              ? (
                <NavDropdown title={`Hello, ${username}!`} id="header-dropdown">
                  <NavDropdown.Item onClick={() => route(`/users/${username}`)}>View profile</NavDropdown.Item>
                  <NavDropdown.Item onClick={onLogout}>Log out</NavDropdown.Item>
                </NavDropdown>
              )
              : <Button variant="outline-light" href="/api/twitter_login"><FontAwesomeIcon icon={faTwitter} /> Log in with Twitter</Button>}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
