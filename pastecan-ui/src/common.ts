import { Grammar, languages } from 'prismjs';

type Language = 'clike' | 'java' | 'javascript' | 'python' | 'scala' | 'scheme' | 'typescript';
export type LanguageOption = Language | 'none';

export const languagesMapping: Readonly<{[index in Language]: [Grammar, string]}> = Object.freeze({
  clike: [languages.clike, 'clike'],
  java: [languages.java, 'java'],
  javascript: [languages.javascript, 'js'],
  python: [languages.python, 'py'],
  scala: [languages.scala, 'scala'],
  scheme: [languages.scheme, 'scheme'],
  typescript: [languages.typescript, 'ts'],
});

export const languagesList: Readonly<LanguageOption[]> = Object.freeze(['none', ...Object.keys(languagesMapping) as Language[]]);

export const exposureList = Object.freeze(['Public', 'Private']) as Readonly<['Public', 'Private']>;
export const MAX_PASTE_SIZE = 20000;
