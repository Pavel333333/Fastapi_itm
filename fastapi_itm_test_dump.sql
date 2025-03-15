--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Ubuntu 17.2-1.pgdg24.04+1)
-- Dumped by pg_dump version 17.2 (Ubuntu 17.2-1.pgdg24.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    path character varying NOT NULL,
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: documents_text; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents_text (
    id_doc integer NOT NULL,
    text character varying NOT NULL,
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.documents_text OWNER TO postgres;

--
-- Name: documents_text_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_text_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_text_id_seq OWNER TO postgres;

--
-- Name: documents_text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_text_id_seq OWNED BY public.documents_text.id;


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: documents_text id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents_text ALTER COLUMN id SET DEFAULT nextval('public.documents_text_id_seq'::regclass);


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (path, id, created_at, updated_at) FROM stdin;
/home/pavel/dev/fastapi_itm/documents_for_tests/gratis-png-yandex.png	1	2025-03-15 14:43:44.521717	2025-03-15 14:43:44.521717
/home/pavel/dev/fastapi_itm/documents_for_tests/d10c58e.jpeg	2	2025-03-15 14:43:44.581931	2025-03-15 14:43:44.581931
/home/pavel/dev/fastapi_itm/documents_for_tests/fgh.jpeg	3	2025-03-15 14:43:44.644428	2025-03-15 14:43:44.644428
\.


--
-- Data for Name: documents_text; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents_text (id_doc, text, id, created_at, updated_at) FROM stdin;
1	Яндекс\r\n	1	2025-03-15 14:43:45.463334	2025-03-15 14:43:45.463334
2	Yandex\r\n	2	2025-03-15 14:43:46.095694	2025-03-15 14:43:46.095694
3	Название принципа\r\n1. Single Responsibility PrincipIe\r\n(Прннцнп единственной обязанности)\r\n2. Ореп Closed Princip1e\r\n(Принцип открытоспсзакрытостн)\r\nЗ. Liskov's Substitution Princip1e\r\n(Принцип подстановки Барбары Лисков)\r\n4. Interface Segregation Princip1e\r\n(Принцип разделения интерфейса)\r\nS. Dependency Inversion Prtncip1e\r\n(Принцип инверсии зависимостей)\r\nОписание\r\nНа каждый объект до.тжна быть возложена одна\r\nединственная обязанность.\r\nПрогразсмные сушности должны быть открыты\r\nхтя расширения, но закрыты хтя изменения.\r\nОбъекты в программе могут быть заменены их\r\nнаследниками без изменения свойств\r\nпротраммы.\r\nМного специализированных интерфейсов\r\nлучше, чем один универса:ъный.\r\nЗависимости внутри системы строятся на\r\nоснове абстракций . Модули верхнего уровня не\r\nзависят от модулей нижнего уровня.\r\nАбстракции не должны зависеть от деталей.\r\nти должны зависеть от\r\nй.\r\n	3	2025-03-15 14:43:47.035956	2025-03-15 14:43:47.035956
\.


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 5, true);


--
-- Name: documents_text_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_text_id_seq', 3, true);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: documents_text documents_text_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents_text
    ADD CONSTRAINT documents_text_pkey PRIMARY KEY (id);


--
-- Name: documents_text documents_text_id_doc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents_text
    ADD CONSTRAINT documents_text_id_doc_fkey FOREIGN KEY (id_doc) REFERENCES public.documents(id);


--
-- PostgreSQL database dump complete
--

