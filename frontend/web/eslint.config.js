// eslint.config.js
export default {
  languageOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  files: ['**/*.js'],
  ignores: [
    'node_modules/**',
    '.svelte-kit/**',
    'build/**',
    '**/*.svelte', // Explicitly ignore Svelte files for now
  ],
  rules: {
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'no-console': ['warn', { allow: ['warn', 'error'] }],
  },
};
