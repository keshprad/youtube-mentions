import App from './App.svelte';

const app = new App({
  target: document.body,
  props: {
    domain: 'http://localhost:8000',
  },
});

export default app;
