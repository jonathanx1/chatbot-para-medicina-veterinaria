-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-04-2025 a las 07:02:26
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `chatbot_veterinario`
--
CREATE DATABASE IF NOT EXISTS `chatbot_veterinario` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `chatbot_veterinario`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultas`
--

CREATE TABLE `consultas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `consulta` text NOT NULL,
  `respuesta` text NOT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consultas`
--

INSERT INTO `consultas` (`id`, `usuario_id`, `consulta`, `respuesta`, `fecha`) VALUES
(1, 1, 'mi perro tiene tos', 'Traqueobronquitis', '2025-04-10 18:25:06'),
(2, 2, 'mi gato tiene diarrea', 'Parvovirus', '2025-04-11 10:26:02'),
(4, 2, 'mi perro tiene fiebre y tos seca', 'Moquillo', '2025-04-11 10:39:00'),
(5, 2, 'mi perro tiene fiebre leve y tos seca', 'Moquillo', '2025-04-11 10:39:25'),
(6, 2, 'mi perro tiene tos y fiebre', 'Moquillo', '2025-04-11 10:39:49'),
(7, 2, 'mi perro tiene fiebre leve y tos seca', 'Moquillo', '2025-04-11 10:46:48'),
(8, 1, 'mi gato tiene fiebre leve y tos seca', 'Moquillo', '2025-04-11 10:48:34'),
(9, 1, 'mi perro tiene fiebre leve y tos seca', 'Desconocido', '2025-04-11 11:06:00'),
(11, 1, 'mi perro tiene fiebre leve  tos seca', 'Desconocido', '2025-04-11 11:15:11'),
(12, 1, 'mi perro tiene fiebre', 'Desconocido', '2025-04-11 11:21:06'),
(13, 1, 'mi perro tiene fiebre leve y tos seca', 'Desconocido', '2025-04-11 11:26:53'),
(14, 1, 'mi perro tiene fiebre leve y tos seca', 'Desconocido', '2025-04-11 11:37:51'),
(15, 1, 'mi perro tiene fiebre levey tos seca', 'Desconocido', '2025-04-11 11:45:35'),
(16, 1, 'mi perro tiene tos seca y fiebre leve', 'Desconocido', '2025-04-11 11:50:59'),
(17, 1, 'mi perro tiene tos ', 'Desconocido', '2025-04-11 11:51:18'),
(18, 1, 'mi perro tiene fiebre ', 'Desconocido', '2025-04-11 12:01:05'),
(23, 1, 'mi perro tiene diarrea', 'Parvovirus', '2025-04-11 17:58:41'),
(24, 1, 'mi perro tiene fiebre', 'Moquillo', '2025-04-11 18:57:18'),
(27, 2, 'mi gato tiene diarrea', 'Parvovirus', '2025-04-11 22:34:23'),
(28, 2, 'mi gato tiene diarrea', 'Parvovirus', '2025-04-11 22:34:23'),
(29, 5, 'mi perro tiene tos', 'Traqueobronquitis', '2025-04-11 22:35:15'),
(30, 5, 'mi perro tiene fiebre', 'Moquillo', '2025-04-11 22:41:08'),
(31, 5, 'mi perro tiene dolor de cabeza', 'Sin coincidencias', '2025-04-11 22:41:54'),
(32, 1, 'mi perro tiene dolor de cabeza', 'Parvovirus', '2025-04-11 22:50:06'),
(33, 1, 'mi perro tiene dolor de cabeza', 'Parvovirus', '2025-04-13 20:24:30'),
(34, 5, 'mi gato tiene dolor de cabeza', 'Parvovirus', '2025-04-13 20:35:47'),
(35, 5, 'mi perro tiene dolor de cabeza', 'Parvovirus', '2025-04-13 21:06:43'),
(36, 5, 'mi perro tiene dolor de cabeza\r\n', 'Parvovirus', '2025-04-13 21:09:22'),
(37, 5, 'mi perro tiene dolor de cabeza', 'Parvovirus', '2025-04-13 21:14:02'),
(38, 5, 'mi perro tiene dolor de cabza', 'Sin coincidencias', '2025-04-13 22:45:10'),
(39, 5, 'mi perro tiene dolor de cabeza\r\n\r\n', 'Parvovirus', '2025-04-13 22:45:23'),
(40, 5, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-13 22:46:53'),
(41, 5, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-13 22:48:15'),
(42, 5, 'mi perro tiene dolor de cabeza\r\n', 'Traqueobronquitis', '2025-04-13 22:48:51'),
(43, 1, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-13 23:09:07'),
(44, 1, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-13 23:41:21'),
(45, 1, 'mi perro tiene dolor de cabeza\r\n\r\n', 'Traqueobronquitis', '2025-04-14 00:01:40'),
(46, 1, 'mi perro tiene fiebre', 'Traqueobronquitis', '2025-04-14 00:03:37'),
(47, 1, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-14 00:04:09'),
(48, 5, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-14 01:24:14'),
(49, 1, 'mi perro tiene dolor de cabeza', 'Traqueobronquitis', '2025-04-27 22:32:53'),
(50, 1, 'mi perro tiene dolor de cabeza', 'migraña', '2025-04-27 22:56:06'),
(51, 1, 'mi perro tiene tos y fiebre', 'Parvovirus', '2025-04-27 22:57:16'),
(52, 2, 'mi perro tiene dolor de cabeza', 'migraña', '2025-04-27 22:59:07'),
(53, 5, 'mi perro tiene tos y secrecion nasal', 'Parvovirus', '2025-04-27 23:16:38'),
(54, 5, 'mi perro tiene tos y secrecion nasal', 'Parvovirus', '2025-04-27 23:18:03'),
(55, 5, 'mi perro tiene dolor de cabeza', 'migraña', '2025-04-27 23:18:47'),
(56, 1, 'mi perro tiene tos pero no fiebre', 'Parvovirus', '2025-04-28 00:49:40'),
(57, 1, 'mi perro no tiene fiebre pero si tos seca', 'Parvovirus', '2025-04-28 00:54:55'),
(58, 1, 'mi perro no tiene fiebre pero si tos seca', 'Parvovirus', '2025-04-28 01:54:14'),
(59, 1, 'mi perro no tiene fiebre pero si tos seca', 'Parvovirus', '2025-04-28 02:11:12'),
(60, 1, 'mi perro no tiene fiebre pero sí tos seca', 'Parvovirus', '2025-04-28 02:17:39'),
(61, 1, 'mi perro no tiene fiebre pero sí tos seca\r\n', 'Parvovirus', '2025-04-28 02:27:29'),
(62, 1, 'mi perro no tiene fiebre pero sí tos seca\r\n', 'Parvovirus', '2025-04-28 02:30:57'),
(63, 1, 'mi perro no tiene fiebre pero sí tos seca\r\n', 'Parvovirus', '2025-04-28 02:31:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `enfermedades`
--

CREATE TABLE `enfermedades` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `sintomas` text NOT NULL,
  `tratamiento` text NOT NULL,
  `prevencion` text NOT NULL,
  `especie_id` int(11) DEFAULT NULL,
  `clase_ml` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `enfermedades`
--

INSERT INTO `enfermedades` (`id`, `nombre`, `sintomas`, `tratamiento`, `prevencion`, `especie_id`, `clase_ml`) VALUES
(1, 'Parvovirus', 'Vómito, diarrea, fiebre', 'Hidratación, antivirales', 'Vacunación', 1, 0),
(2, 'Moquillo', 'Fiebre, tos, secreción nasal', 'Suero, antibióticos', 'Vacunación', 1, 1),
(3, 'Traqueobronquitis', 'Tos seca, fiebre leve', 'Antibióticos, antiinflamatorios', 'Evitar contacto con perros enfermos', 1, 2),
(5, 'migraña', 'dolor de cabeza', 'pastillas', 'evitar el frio', 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `especies`
--

CREATE TABLE `especies` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `especies`
--

INSERT INTO `especies` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Canino', 'Perros domésticos de diversas razas, caracterizados por su lealtad, sociabilidad y necesidad de ejercicio regular. Incluye razas desde pequeños chihuahuas hasta grandes labradores.'),
(2, 'Felino', 'Gatos domésticos conocidos por su independencia, agilidad y adaptabilidad. Comprende razas variadas, desde siameses hasta persas, y son excelentes compañeros en el hogar.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `comentario` text DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `feedback`
--

INSERT INTO `feedback` (`id`, `usuario_id`, `comentario`, `rating`, `fecha`) VALUES
(1, 1, 'buena aplicacion', 5, '2025-04-11 15:06:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varbinary(255) NOT NULL,
  `email` varbinary(255) NOT NULL,
  `rol` varbinary(50) NOT NULL,
  `password` varbinary(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `rol`, `password`) VALUES
(1, 0xee01dbdec3242fe2de10aa80aa4b8b77, 0x5f8bc2a2cf9353f95a1122825a114051fdad40eaff3936e89459e79a4c27a85a, 0xee1c0c972b642280acca6f6340923851, 0xec9774afa576d1487a9e6d5dc59c145a),
(2, 0x5b33656b9224fed9c0f320d55ac03890, 0x248893139949f29a50785b033bf9908a11a59fcdb33d354da4dfd347e49520ca, 0x01bdbf51124bdad361f242ce40d1b269, 0x421dc395ef1fa81d86a98dbaffd1e56e),
(5, 0x2e68e5f87c198c3ad05de26133a60586, 0x5bd7ca92b50b384233911e75ed16d12bfdad40eaff3936e89459e79a4c27a85a, 0x7a1de14a6053208217886d35e3939c41, 0x0d8ffdedb474a759959a195aad09aa4d);

--
-- Disparadores `usuarios`
--
DELIMITER $$
CREATE TRIGGER `set_default_rol` BEFORE INSERT ON `usuarios` FOR EACH ROW BEGIN
    IF NEW.rol IS NULL OR NEW.rol = '' THEN
        SET NEW.rol = AES_ENCRYPT('estudiante', 'mi_clave_secreta');
    END IF;
END
$$
DELIMITER ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `enfermedades`
--
ALTER TABLE `enfermedades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `especie_id` (`especie_id`);

--
-- Indices de la tabla `especies`
--
ALTER TABLE `especies`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `consultas`
--
ALTER TABLE `consultas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT de la tabla `enfermedades`
--
ALTER TABLE `enfermedades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `especies`
--
ALTER TABLE `especies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD CONSTRAINT `consultas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `enfermedades`
--
ALTER TABLE `enfermedades`
  ADD CONSTRAINT `enfermedades_ibfk_1` FOREIGN KEY (`especie_id`) REFERENCES `especies` (`id`);

--
-- Filtros para la tabla `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
