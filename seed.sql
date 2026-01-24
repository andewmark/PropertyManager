--
-- devQL database dump
--

\restrict tDq4o6zexuY7W085A36gHjHi1qLATCRGIXhHSIQvvMqSurj63B9OPcksiBZRhyH

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

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
-- Data for Name: tbl_address; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_address (address_id, street_number, city, state, postal_code, country, street) VALUES (1, '123', 'Boston', 'MA', '02118', 'USA', 'Maple Street');


--
-- Data for Name: tbl_building_type; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (1, 'Single-Family');
INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (2, 'Duplex');
INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (3, 'Triplex');
INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (4, 'Quadplex');
INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (5, 'Muilt-Unit');
INSERT INTO public.tbl_building_type (building_type_id, building_type) VALUES (6, 'Townhome');


--
-- Data for Name: tbl_property; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_property (property_id, property_name, multi_unit) VALUES (1, 'Maple Grove Apartments', true);


--
-- Data for Name: tbl_building; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_building (building_id, property_id, address_id, building_name, building_type_id, is_main_building) VALUES (1, 1, 1, 'Building A', 5, true);


--
-- Data for Name: tbl_tenants; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_tenants (tenant_id, first_name, middle_name, family_name, email, phone, emergency_contact_first_name, "emergency_contact_middle_Initial", emergency_contact_family_name, emergency_contact_phone) VALUES (2, 'Jane', NULL, 'Smith', 'jane.smith@email.com', '617-555-5678', 'Thomas', 'P', 'Mark', '617-555-7890');
INSERT INTO public.tbl_tenants (tenant_id, first_name, middle_name, family_name, email, phone, emergency_contact_first_name, "emergency_contact_middle_Initial", emergency_contact_family_name, emergency_contact_phone) VALUES (1, 'John', 'Thomas', 'Doe', 'john.doe@email.com', '617-555-1234', 'Jane', 'A', 'Doe', '617-555-7541');


--
-- Data for Name: tbl_units; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_units (unit_id, building_id, unit_number, square_feet, beds, baths, market_rent) VALUES (1, 1, '1A', 750, 1, 1, 1200.00);
INSERT INTO public.tbl_units (unit_id, building_id, unit_number, square_feet, beds, baths, market_rent) VALUES (2, 1, '1B', 820, 2, 1, 1600.00);


--
-- Data for Name: tbl_lease; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_lease (lease_id, tenant_id, unit_id, start_date, end_date, move_out_date, rent, security_deposit) VALUES (1, 1, 1, '2025-08-01', '2026-07-31', NULL, 1200.00, 0.00);


--
-- Data for Name: tbl_charges; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_charges (charge_id, lease_id, charge_type, amount, due_date, period_start, period_end, status, created_at) VALUES (1, 1, 'rent', 1200.00, '2026-01-01', '2026-01-01', '2026-01-31', 'partial', '2026-01-11 11:42:55');
INSERT INTO public.tbl_charges (charge_id, lease_id, charge_type, amount, due_date, period_start, period_end, status, created_at) VALUES (2, 1, 'rent', 1200.00, '2026-02-01', '2026-02-01', '2026-02-28', 'unpaid', '2026-01-11 11:42:55');
INSERT INTO public.tbl_charges (charge_id, lease_id, charge_type, amount, due_date, period_start, period_end, status, created_at) VALUES (3, 1, 'late_fee', 75.00, '2026-01-10', NULL, NULL, 'unpaid', '2026-01-11 11:42:55');


--
-- Data for Name: tbl_expense_category; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_expense_category (category_id, category_name, category_group) VALUES (1, 'Utilities', 'operating');
INSERT INTO public.tbl_expense_category (category_id, category_name, category_group) VALUES (2, 'Maintenance', 'operating');
INSERT INTO public.tbl_expense_category (category_id, category_name, category_group) VALUES (3, 'Insurance', 'fixed');
INSERT INTO public.tbl_expense_category (category_id, category_name, category_group) VALUES (4, 'Property Tax', 'fixed');
INSERT INTO public.tbl_expense_category (category_id, category_name, category_group) VALUES (5, 'Cleaning', 'operating');


--
-- Data for Name: tbl_vendors; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_vendors (vendor_id, vendor_name, phone, email) VALUES (1, 'City Electric Co', '800-111-2222', 'billing@cityelectric.com');


--
-- Data for Name: tbl_maintenance; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_maintenance (maintenance_request_id, unit_id, tenant_id, description, priority, status, date_requested, date_completed, vendor_id) VALUES (2, 1, 1, 'Leaking kitchen sink', 'High', 'In Progress', '2024-02-10', NULL, 1);


--
-- Data for Name: tbl_recurring_expenses; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_recurring_expenses (recurring_rule_id, property_id, building_id, unit_id, vendor_id, category_id, description, amount, start_date, end_date, payment_method, active, frequency) VALUES (2, 1, 1, NULL, 1, 1, 'Monthly electric service', 450.00, '2024-01-01', NULL, 'Check', true, '1 day');


--
-- Data for Name: tbl_property_expenses; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_property_expenses (expense_id, property_id, building_id, unit_id, vendor_id, expense_category_id, description, expense_amount, date_incurred, date_paid, payment_method, recurring_rule_id) VALUES (2, 1, 1, NULL, 1, 1, 'Electric bill ??? January', 462.35, '2024-01-05', '2024-01-10', 'Check', 2);
INSERT INTO public.tbl_property_expenses (expense_id, property_id, building_id, unit_id, vendor_id, expense_category_id, description, expense_amount, date_incurred, date_paid, payment_method, recurring_rule_id) VALUES (4, 1, 1, 1, 1, 2, 'Kitchen sink repair ??? Unit 1A', 275.00, '2024-02-12', '2024-02-15', 'Credit/Debit Card', NULL);


--
-- Data for Name: tbl_documents; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_documents (document_id, property_id, unit_id, expense_id, request_id, stored_filename, orginal_filename, file_path, file_type, file_size, storage_location, uploaded_at, lease_id) VALUES (1, 1, 1, NULL, NULL, 'lease_1a_2024.pdf', 'Lease_John_Doe.pdf', '/documents/leases/', 'application/pdf', '245000', 's3', '2026-01-02 21:00:47.374581', 1);


--
-- Data for Name: tbl_images; Type: TABLE DATA; Schema: public; Owner: dev
--



--
-- Data for Name: tbl_payments; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_payments (payment_id, lease_id, payment_amount, payment_date, payment_method, payment_status) VALUES (1, 1, 600.00, '2026-01-05', 'Credit/Debit Card', 'Completed');


--
-- Data for Name: tbl_payment_applications; Type: TABLE DATA; Schema: public; Owner: dev
--

INSERT INTO public.tbl_payment_applications (application_id, payment_id, charge_id, amount_applied, created_at) VALUES (1, 1, 1, 600.00, '2026-01-11 11:44:46');


--
-- Name: tbl_address_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_address_address_id_seq', 1, true);


--
-- Name: tbl_building_building_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_building_building_id_seq', 1, true);


--
-- Name: tbl_building_type_building_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_building_type_building_type_id_seq', 6, true);


--
-- Name: tbl_documents_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_documents_document_id_seq', 1, true);


--
-- Name: tbl_expense_category_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_expense_category_category_id_seq', 5, true);


--
-- Name: tbl_images_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_images_image_id_seq', 1, false);


--
-- Name: tbl_lease_lease_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_lease_lease_id_seq', 1, true);


--
-- Name: tbl_maintenance_maintenance_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_maintenance_maintenance_request_id_seq', 2, true);


--
-- Name: tbl_payments_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_payments_payment_id_seq', 2, true);


--
-- Name: tbl_property_expenses_expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_property_expenses_expense_id_seq', 4, true);


--
-- Name: tbl_property_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_property_property_id_seq', 1, true);


--
-- Name: tbl_recurring_expenses_recurring_rule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_recurring_expenses_recurring_rule_id_seq', 2, true);


--
-- Name: tbl_tenants_tenant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_tenants_tenant_id_seq', 2, true);


--
-- Name: tbl_units_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_units_unit_id_seq', 2, true);


--
-- Name: tbl_vendors_vendor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('public.tbl_vendors_vendor_id_seq', 1, true);

--
-- devQL database dump complete
--

\unrestrict tDq4o6zexuY7W085A36gHjHi1qLATCRGIXhHSIQvvMqSurj63B9OPcksiBZRhyH

