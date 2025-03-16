/** @type {import('./$types').PageLoad} */
export function load({ fetch, params }) {
  // This function runs on both server and client
  // We'll return an empty object for now and let the component handle data fetching
  return {
    suggestions: [],
    warning: null
  };
} 