import { LanguageOption } from '../common';

export type GetPasteData = {
    content: string;
    date: string;
    id: string;
    language: LanguageOption;
    title: string;
    screenName: string;
    exposure: 'Public' | 'Private';
};

export type GetPastesData = {
    date: string;
    id: string;
    language: LanguageOption;
    title: string;
    screenName: string;
    exposure: 'Public' | 'Private';
};

export type GetPastesResponse = {
    items: GetPastesData[];
    count: number;
};
