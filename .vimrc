"--------------------------------------------------
" set
"--------------------------------------------------

set sm
" automatic indentation
set ai
" no auto line wrapping
set nowrap
" use kawaii menu
set wildmenu
" use tab for autocomplete
set wcm=<TAB>

" turn on automatic syntax highlighting
syntax on

"--------------------------------------------------
" color
"--------------------------------------------------

"set background=light
"colorscheme solarized
"colorscheme xoria256m

"--------------------------------------------------
" encoding
"--------------------------------------------------

set encoding=utf-8
set termencoding=utf-8

map =w :e ++enc=cp1251<CR>
map =d :e ++enc=ibm866<CR>
map =k :e ++enc=koi8-r<CR>
map =u :e ++enc=utf-8<CR>

" <F8> Change encoding
menu Encoding.cp1251 :e ++enc=cp1251<CR>
menu Encoding.cp866  :e ++enc=ibm866<CR>
menu Encoding.koi8-r :e ++enc=koi8-r<CR>
menu Encoding.utf-8  :e ++enc=utf-8<CR>
map  <F8> :emenu Encoding.<TAB>

" <F9> Convert file encoding 
menu FEnc.cp1251    :set fenc=cp1251<CR>
menu FEnc.cp866     :set fenc=ibm866<CR>
menu FEnc.koi8-r    :set fenc=koi8-r<CR>
menu FEnc.utf-8     :set fenc=utf-8<CR>
menu FEnc.ucs-2le   :set fenc=ucs-2le<CR>
map  <F9> :emenu FEnc.<Tab>

"--------------------------------------------------
" indenting
"--------------------------------------------------

set smartindent 	" autoindent
set shiftwidth=4	" autoindent width
set tabstop=4		" number of spaces to make a tab
" set expandtab		" use spaces instead of tabs

"--------------------------------------------------
" pathogen
"--------------------------------------------------

execute pathogen#infect()
filetype plugin indent on

"--------------------------------------------------
" powerline
"--------------------------------------------------

let g:Powerline_symbols = 'compatible'
set laststatus=2
