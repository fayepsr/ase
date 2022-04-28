import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

const url =
  'https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/api/v1/highlight';

test('should correctly set defaults', () => {
  render(<App />);

  // Default language is set to Java
  expect(screen.getByText('Java').selected).toBeTruthy();
  expect(screen.getByText('Python').selected).toBeFalsy();
  expect(screen.getByText('Kotlin').selected).toBeFalsy();

  // Code text area should be empty
  expect(screen.getByLabelText('Code:')).toHaveTextContent('');

  // Result and error are not displayed
  expect(screen.queryByTestId('result')).not.toBeInTheDocument();
  expect(screen.queryByTestId('error')).not.toBeInTheDocument();
});

test('should simulate language selection', async () => {
  render(<App />);
  userEvent.selectOptions(screen.getByLabelText('Language:'), 'python');
  expect(screen.getByText('Python').selected).toBeTruthy();
  expect(screen.getByText('Java').selected).toBeFalsy();
  expect(screen.getByText('Kotlin').selected).toBeFalsy();
});

test('should simulate entering code in text area', async () => {
  render(<App />);
  userEvent.type(screen.getByLabelText('Code:'), 'print("hello world")');
  expect(screen.getByLabelText('Code:')).toHaveTextContent(
    'print("hello world")'
  );
});

test('should simulate success on button click and display result', async () => {
  render(<App />);

  const server = setupServer(
    rest.post(url, (_, res, ctx) => {
      return res(
        ctx.status(200),
        ctx.json({ resp: Buffer.from('Success').toString('base64') })
      );
    })
  );
  server.listen();

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('result')).toBeInTheDocument();
  expect(screen.getByTestId('result')).toHaveTextContent('Success');

  server.close();
});

test('should simulate error on button click and display error', async () => {
  render(<App />);

  const server = setupServer(
    rest.post(url, (_, res, ctx) => {
      return res(ctx.status(500), ctx.text('msg: Error'));
    })
  );
  server.listen();

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('error')).toBeInTheDocument();
  expect(screen.getByTestId('error')).toHaveTextContent('Error');

  server.close();
});

test('should display result and remove previous error on success after error', async () => {
  render(<App />);

  const server = setupServer(
    rest.post(url, (_, res, ctx) => {
      return res(ctx.status(500), ctx.text('msg: Error'));
    })
  );
  server.listen();

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('error')).toBeInTheDocument();
  expect(screen.getByTestId('error')).toHaveTextContent('Error');

  server.use(
    rest.post(url, (_, res, ctx) => {
      return res(
        ctx.status(200),
        ctx.json({ resp: Buffer.from('Success').toString('base64') })
      );
    })
  );

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('result')).toBeInTheDocument();
  expect(screen.getByTestId('result')).toHaveTextContent('Success');
  expect(screen.queryByTestId('error')).not.toBeInTheDocument();

  server.close();
});

test('should display error and remove previous result on error after success', async () => {
  render(<App />);

  const server = setupServer(
    rest.post(url, (_, res, ctx) => {
      return res(
        ctx.status(200),
        ctx.json({ resp: Buffer.from('Success').toString('base64') })
      );
    })
  );
  server.listen();

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('result')).toBeInTheDocument();
  expect(screen.getByTestId('result')).toHaveTextContent('Success');

  server.use(
    rest.post(url, (_, res, ctx) => {
      return res(ctx.status(500), ctx.text('msg: Error'));
    })
  );
  server.listen();

  userEvent.click(screen.getByText('Submit'));
  expect(await screen.findByTestId('error')).toBeInTheDocument();
  expect(screen.getByTestId('error')).toHaveTextContent('Error');
  expect(screen.queryByTestId('result')).not.toBeInTheDocument();

  server.close();
});
