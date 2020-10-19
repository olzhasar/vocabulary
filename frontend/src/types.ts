export interface RootState {
  token: string | null;
  authError: string | null;
  words: Array<object>;
}
