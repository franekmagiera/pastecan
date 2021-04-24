import { h } from 'preact';
import { useState, StateUpdater } from 'preact/hooks';
import { highlight } from 'prismjs';
import 'prismjs/components/prism-clike.js';
import 'prismjs/components/prism-java.js';
import 'prismjs/components/prism-javascript.js';
import 'prismjs/components/prism-python.js';
import 'prismjs/components/prism-scala.js';
import 'prismjs/components/prism-scheme.js';
import 'prismjs/components/prism-typescript.js';
import 'prismjs/themes/prism.css';
import Editor from 'react-simple-code-editor';
import { LanguageOption, languagesMapping } from '../common';

interface PasteProps {
  language: LanguageOption;
  pasteContent: string;
  readOnly: boolean;
  onContentChange?: StateUpdater<string>;
}

const Paste = (props: PasteProps) => {
  const {
    language,
    pasteContent,
    readOnly,
    onContentChange,
  } = props;

  const highlightCode = (code: string, lang: LanguageOption) => {
    if (lang === 'none') {
      return code;
    }
    const grammar = languagesMapping[lang][0];
    const highlightLang = languagesMapping[lang][1];
    return highlight(code, grammar, highlightLang);
  };

  return (
    <div className="pasteEditor">
      <Editor
        value={pasteContent}
        onValueChange={(text) => (onContentChange ? onContentChange(text) : null)}
        highlight={(text) => highlightCode(text, language)}
        padding={10}
        style={{
          fontFamily: '"Fira code", "Fira Mono", monospace',
          fontSize: 14,
          backgroundColor: '#f5f2f0',
        }}
        readOnly={readOnly}
        textareaClassName="pasteTextarea"
      />
    </div>
  );
};

Paste.defaultProps = { onContentChange: undefined };

export default Paste;
