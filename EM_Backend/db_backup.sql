--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-12-26 00:07:10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16591)
-- Name: em_schema; Type: SCHEMA; Schema: -; Owner: em_user
--

CREATE SCHEMA em_schema;


ALTER SCHEMA em_schema OWNER TO em_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16611)
-- Name: user_budget; Type: TABLE; Schema: em_schema; Owner: postgres
--

CREATE TABLE em_schema.user_budget (
    budget_id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    category character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE em_schema.user_budget OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16599)
-- Name: user_expense; Type: TABLE; Schema: em_schema; Owner: postgres
--

CREATE TABLE em_schema.user_expense (
    expense_id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    category character varying(100),
    description text,
    date date
);


ALTER TABLE em_schema.user_expense OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16592)
-- Name: user_signup; Type: TABLE; Schema: em_schema; Owner: em_user
--

CREATE TABLE em_schema.user_signup (
    user_id integer NOT NULL,
    user_name character varying(50),
    email character varying(50),
    password character varying(50)
);


ALTER TABLE em_schema.user_signup OWNER TO em_user;

--
-- TOC entry 4852 (class 0 OID 16611)
-- Dependencies: 218
-- Data for Name: user_budget; Type: TABLE DATA; Schema: em_schema; Owner: postgres
--

COPY em_schema.user_budget (budget_id, user_id, amount, category, created_at) FROM stdin;
\.


--
-- TOC entry 4851 (class 0 OID 16599)
-- Dependencies: 217
-- Data for Name: user_expense; Type: TABLE DATA; Schema: em_schema; Owner: postgres
--

COPY em_schema.user_expense (expense_id, user_id, amount, category, description, date) FROM stdin;
\.


--
-- TOC entry 4850 (class 0 OID 16592)
-- Dependencies: 216
-- Data for Name: user_signup; Type: TABLE DATA; Schema: em_schema; Owner: em_user
--

COPY em_schema.user_signup (user_id, user_name, email, password) FROM stdin;
1	hemal	dfdbh@gmail.com	11111
2	hemal_dholakiya	hemaldholakiya@222gmail.com	22222
3	hemal	hemaldholakiya12@gmail.com	77777
4	abc	hemaldholakiya214@gmail.com	33333
\.


--
-- TOC entry 4704 (class 2606 OID 16616)
-- Name: user_budget pk_budget_id; Type: CONSTRAINT; Schema: em_schema; Owner: postgres
--

ALTER TABLE ONLY em_schema.user_budget
    ADD CONSTRAINT pk_budget_id PRIMARY KEY (budget_id);


--
-- TOC entry 4702 (class 2606 OID 16605)
-- Name: user_expense pk_expense_id; Type: CONSTRAINT; Schema: em_schema; Owner: postgres
--

ALTER TABLE ONLY em_schema.user_expense
    ADD CONSTRAINT pk_expense_id PRIMARY KEY (expense_id);


--
-- TOC entry 4698 (class 2606 OID 16596)
-- Name: user_signup primary_key_user_id; Type: CONSTRAINT; Schema: em_schema; Owner: em_user
--

ALTER TABLE ONLY em_schema.user_signup
    ADD CONSTRAINT primary_key_user_id PRIMARY KEY (user_id);


--
-- TOC entry 4700 (class 2606 OID 16598)
-- Name: user_signup unique_email; Type: CONSTRAINT; Schema: em_schema; Owner: em_user
--

ALTER TABLE ONLY em_schema.user_signup
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- TOC entry 4705 (class 2606 OID 16606)
-- Name: user_expense fk_user_id; Type: FK CONSTRAINT; Schema: em_schema; Owner: postgres
--

ALTER TABLE ONLY em_schema.user_expense
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES em_schema.user_signup(user_id);


--
-- TOC entry 4706 (class 2606 OID 16617)
-- Name: user_budget fk_user_id; Type: FK CONSTRAINT; Schema: em_schema; Owner: postgres
--

ALTER TABLE ONLY em_schema.user_budget
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES em_schema.user_signup(user_id);


-- Completed on 2024-12-26 00:07:10

--
-- PostgreSQL database dump complete
--

