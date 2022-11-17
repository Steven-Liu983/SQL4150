-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 17, 2022 at 02:14 AM
-- Server version: 5.7.24
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hostel`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(25) NOT NULL,
  `password` text NOT NULL,
  `role` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`, `role`) VALUES
(1, 'admin@email.com', 'pbkdf2:sha256:260000$8Q4XfaNA89L9xe3p$6dbd1aeb435c8bad3112534678a4aa03169d728df277c748fd9e3eb03111c3c9', 'Administrator');

-- --------------------------------------------------------

--
-- Table structure for table `advisor`
--

CREATE TABLE `advisor` (
  `advisor_id` int(11) NOT NULL,
  `department` varchar(25) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `room_num` int(11) NOT NULL,
  `staff_num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `advisor`
--

INSERT INTO `advisor` (`advisor_id`, `department`, `phone`, `room_num`, `staff_num`) VALUES
(10001, 'Science', '2261234567', 125, 100001);

-- --------------------------------------------------------

--
-- Table structure for table `flats_rooms`
--

CREATE TABLE `flats_rooms` (
  `place_num` int(11) NOT NULL,
  `room_num` int(11) NOT NULL,
  `monthly_rent` float NOT NULL,
  `flat_num` int(11) NOT NULL,
  `capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flats_rooms`
--

INSERT INTO `flats_rooms` (`place_num`, `room_num`, `monthly_rent`, `flat_num`, `capacity`) VALUES
(1001, 1001, 699.95, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `hall_res`
--

CREATE TABLE `hall_res` (
  `hall_num` int(11) NOT NULL,
  `hall_name` varchar(25) NOT NULL,
  `hall_address` varchar(50) NOT NULL,
  `hall_phone` varchar(20) NOT NULL,
  `staff_num` int(11) NOT NULL,
  `capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `hall_res`
--

INSERT INTO `hall_res` (`hall_num`, `hall_name`, `hall_address`, `hall_phone`, `staff_num`, `capacity`) VALUES
(1, 'Wilson', '2635 Third Street', '2263625872', 100002, 79);

-- --------------------------------------------------------

--
-- Table structure for table `hall_rooms`
--

CREATE TABLE `hall_rooms` (
  `place_num` int(11) NOT NULL,
  `room_num` int(11) NOT NULL,
  `monthly_rent` float NOT NULL,
  `hall_num` int(11) NOT NULL,
  `capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `hall_rooms`
--

INSERT INTO `hall_rooms` (`place_num`, `room_num`, `monthly_rent`, `hall_num`, `capacity`) VALUES
(101, 101, 965.95, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `inspection`
--

CREATE TABLE `inspection` (
  `inspect_num` int(11) NOT NULL,
  `staff_num` int(11) NOT NULL,
  `flat_num` int(11) NOT NULL,
  `inspect_date` date NOT NULL,
  `satisfy` varchar(5) NOT NULL,
  `comments` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `inspection`
--

INSERT INTO `inspection` (`inspect_num`, `staff_num`, `flat_num`, `inspect_date`, `satisfy`, `comments`) VALUES
(10, 100003, 1, '2022-11-16', 'Yes', 'Keep up the good work');

-- --------------------------------------------------------

--
-- Table structure for table `invoices_flats`
--

CREATE TABLE `invoices_flats` (
  `invoice_num` int(11) NOT NULL,
  `lease_num` int(11) NOT NULL,
  `payment_due` float NOT NULL,
  `payment_paid` float NOT NULL,
  `payment_date` date NOT NULL,
  `payment_method` varchar(30) NOT NULL,
  `first_reminder` date DEFAULT NULL,
  `second_reminder` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `invoices_flats`
--

INSERT INTO `invoices_flats` (`invoice_num`, `lease_num`, `payment_due`, `payment_paid`, `payment_date`, `payment_method`, `first_reminder`, `second_reminder`) VALUES
(111010, 11101, 0, 5600, '2022-09-02', 'Onlline Banking', '2022-08-30', '2022-09-02');

-- --------------------------------------------------------

--
-- Table structure for table `invoices_halls`
--

CREATE TABLE `invoices_halls` (
  `invoice_num` int(11) NOT NULL,
  `lease_num` int(11) NOT NULL,
  `payment_due` float NOT NULL,
  `payment_paid` float NOT NULL,
  `payment_date` date NOT NULL,
  `payment_method` varchar(30) NOT NULL,
  `first_reminder` date DEFAULT NULL,
  `second_reminder` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `leases_flats`
--

CREATE TABLE `leases_flats` (
  `lease_num` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  `grade_num` int(11) NOT NULL,
  `place_num` int(11) NOT NULL,
  `flat_num` int(11) NOT NULL,
  `lease_start` date NOT NULL,
  `lease_end` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `leases_flats`
--

INSERT INTO `leases_flats` (`lease_num`, `semester`, `grade_num`, `place_num`, `flat_num`, `lease_start`, `lease_end`) VALUES
(11101, 2, 60270768, 1001, 1, '2022-09-05', '2023-04-28');

-- --------------------------------------------------------

--
-- Table structure for table `leases_halls`
--

CREATE TABLE `leases_halls` (
  `lease_num` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  `grade_num` int(11) NOT NULL,
  `place_num` int(11) NOT NULL,
  `hall_num` int(11) NOT NULL,
  `lease_start` date NOT NULL,
  `lease_end` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `leases_halls`
--

INSERT INTO `leases_halls` (`lease_num`, `semester`, `grade_num`, `place_num`, `hall_num`, `lease_start`, `lease_end`) VALUES
(1101, 2, 72269035, 101, 1, '2022-09-05', '2023-04-28');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staff_num` int(11) NOT NULL,
  `fname` varchar(25) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `province` varchar(20) NOT NULL,
  `postcode` varchar(10) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(15) NOT NULL,
  `position` varchar(25) NOT NULL,
  `location` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staff_num`, `fname`, `lname`, `address`, `city`, `province`, `postcode`, `dob`, `gender`, `position`, `location`) VALUES
(100001, 'Robert', 'Williams', '2365 Main Street', 'Windsor', 'Ontario', '21356', '1992-11-05', 'Male', 'Advisor', 'Hostel Office'),
(100002, 'Adam', 'Moore', '3562 Second Street', 'Chatham', 'Ontario', '23685', '1990-11-12', 'Male', 'Hall Manager', 'Hall'),
(100003, 'Jenny', 'Jones', '3628 Fifth Street', 'Windsor', 'Ontario', '29365', '1993-05-16', 'Female', 'Flat Inspector', 'Flats');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `grade_num` int(11) NOT NULL,
  `fname` varchar(25) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `province` varchar(20) NOT NULL,
  `postcode` varchar(10) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(15) NOT NULL,
  `category` varchar(25) NOT NULL,
  `nationality` varchar(25) NOT NULL,
  `special_needs` text,
  `comments` text,
  `status` varchar(10) NOT NULL,
  `major` varchar(20) NOT NULL,
  `advisor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`grade_num`, `fname`, `lname`, `address`, `city`, `province`, `postcode`, `dob`, `gender`, `category`, `nationality`, `special_needs`, `comments`, `status`, `major`, `advisor_id`) VALUES
(26443806, 'Jose', 'Garcia', '2345 Second Street', 'Toronto', 'Ontario', '34265', '2000-04-12', 'Male', 'First-Year Undergrad', 'Mexican', '', '', 'Waiting', 'Physics', 10001),
(60270768, 'Mark', 'Johnson', '2536 Fourth Street', 'London', 'Ontario', '25376', '2001-11-15', 'Male', 'First-Year Undergrad', 'Canadian', '', '', 'Placed', 'Chemistry', 10001),
(72269035, 'John', 'Smith', '1234 First Street', 'Windsor', 'Ontario', '16358', '2000-11-06', 'Male', 'First-Year Undergrad', 'Canadian', 'ADHD', 'Difficult to pay attention in class', 'Placed', 'Computer Science', 10001);

-- --------------------------------------------------------

--
-- Table structure for table `stu_flats`
--

CREATE TABLE `stu_flats` (
  `flat_num` int(11) NOT NULL,
  `flat_address` varchar(50) NOT NULL,
  `avail_room` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `stu_flats`
--

INSERT INTO `stu_flats` (`flat_num`, `flat_address`, `avail_room`) VALUES
(1, '2135 Third Street', 19);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `advisor`
--
ALTER TABLE `advisor`
  ADD PRIMARY KEY (`advisor_id`),
  ADD UNIQUE KEY `staff_num` (`staff_num`);

--
-- Indexes for table `flats_rooms`
--
ALTER TABLE `flats_rooms`
  ADD PRIMARY KEY (`place_num`),
  ADD KEY `flat_num` (`flat_num`);

--
-- Indexes for table `hall_res`
--
ALTER TABLE `hall_res`
  ADD PRIMARY KEY (`hall_num`),
  ADD UNIQUE KEY `staff_num` (`staff_num`);

--
-- Indexes for table `hall_rooms`
--
ALTER TABLE `hall_rooms`
  ADD PRIMARY KEY (`place_num`),
  ADD KEY `hall_num` (`hall_num`);

--
-- Indexes for table `inspection`
--
ALTER TABLE `inspection`
  ADD PRIMARY KEY (`inspect_num`),
  ADD KEY `staff_num` (`staff_num`),
  ADD KEY `flat_num` (`flat_num`);

--
-- Indexes for table `invoices_flats`
--
ALTER TABLE `invoices_flats`
  ADD PRIMARY KEY (`invoice_num`),
  ADD UNIQUE KEY `lease_num` (`lease_num`);

--
-- Indexes for table `invoices_halls`
--
ALTER TABLE `invoices_halls`
  ADD PRIMARY KEY (`invoice_num`),
  ADD UNIQUE KEY `lease_num` (`lease_num`);

--
-- Indexes for table `leases_flats`
--
ALTER TABLE `leases_flats`
  ADD PRIMARY KEY (`lease_num`),
  ADD UNIQUE KEY `grade_num` (`grade_num`),
  ADD KEY `place_num` (`place_num`),
  ADD KEY `flat_num` (`flat_num`);

--
-- Indexes for table `leases_halls`
--
ALTER TABLE `leases_halls`
  ADD PRIMARY KEY (`lease_num`),
  ADD UNIQUE KEY `grade_num` (`grade_num`),
  ADD UNIQUE KEY `place_num` (`place_num`),
  ADD KEY `hall_num` (`hall_num`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staff_num`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`grade_num`),
  ADD KEY `advisor_id` (`advisor_id`);

--
-- Indexes for table `stu_flats`
--
ALTER TABLE `stu_flats`
  ADD PRIMARY KEY (`flat_num`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `advisor`
--
ALTER TABLE `advisor`
  MODIFY `advisor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10002;

--
-- AUTO_INCREMENT for table `flats_rooms`
--
ALTER TABLE `flats_rooms`
  MODIFY `place_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1002;

--
-- AUTO_INCREMENT for table `hall_res`
--
ALTER TABLE `hall_res`
  MODIFY `hall_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `hall_rooms`
--
ALTER TABLE `hall_rooms`
  MODIFY `place_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `inspection`
--
ALTER TABLE `inspection`
  MODIFY `inspect_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `invoices_flats`
--
ALTER TABLE `invoices_flats`
  MODIFY `invoice_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=111011;

--
-- AUTO_INCREMENT for table `invoices_halls`
--
ALTER TABLE `invoices_halls`
  MODIFY `invoice_num` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `leases_flats`
--
ALTER TABLE `leases_flats`
  MODIFY `lease_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11102;

--
-- AUTO_INCREMENT for table `leases_halls`
--
ALTER TABLE `leases_halls`
  MODIFY `lease_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1102;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `staff_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100004;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `grade_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72269036;

--
-- AUTO_INCREMENT for table `stu_flats`
--
ALTER TABLE `stu_flats`
  MODIFY `flat_num` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advisor`
--
ALTER TABLE `advisor`
  ADD CONSTRAINT `advisor_ibfk_1` FOREIGN KEY (`staff_num`) REFERENCES `staff` (`staff_num`);

--
-- Constraints for table `flats_rooms`
--
ALTER TABLE `flats_rooms`
  ADD CONSTRAINT `flats_rooms_ibfk_1` FOREIGN KEY (`flat_num`) REFERENCES `stu_flats` (`flat_num`);

--
-- Constraints for table `hall_res`
--
ALTER TABLE `hall_res`
  ADD CONSTRAINT `hall_res_ibfk_1` FOREIGN KEY (`staff_num`) REFERENCES `staff` (`staff_num`);

--
-- Constraints for table `hall_rooms`
--
ALTER TABLE `hall_rooms`
  ADD CONSTRAINT `hall_rooms_ibfk_1` FOREIGN KEY (`hall_num`) REFERENCES `hall_res` (`hall_num`);

--
-- Constraints for table `inspection`
--
ALTER TABLE `inspection`
  ADD CONSTRAINT `inspection_ibfk_1` FOREIGN KEY (`staff_num`) REFERENCES `staff` (`staff_num`),
  ADD CONSTRAINT `inspection_ibfk_2` FOREIGN KEY (`flat_num`) REFERENCES `stu_flats` (`flat_num`);

--
-- Constraints for table `invoices_flats`
--
ALTER TABLE `invoices_flats`
  ADD CONSTRAINT `invoices_flats_ibfk_1` FOREIGN KEY (`lease_num`) REFERENCES `leases_flats` (`lease_num`);

--
-- Constraints for table `invoices_halls`
--
ALTER TABLE `invoices_halls`
  ADD CONSTRAINT `invoices_halls_ibfk_1` FOREIGN KEY (`lease_num`) REFERENCES `leases_halls` (`lease_num`);

--
-- Constraints for table `leases_flats`
--
ALTER TABLE `leases_flats`
  ADD CONSTRAINT `leases_flats_ibfk_1` FOREIGN KEY (`grade_num`) REFERENCES `student` (`grade_num`),
  ADD CONSTRAINT `leases_flats_ibfk_2` FOREIGN KEY (`place_num`) REFERENCES `flats_rooms` (`place_num`),
  ADD CONSTRAINT `leases_flats_ibfk_3` FOREIGN KEY (`flat_num`) REFERENCES `stu_flats` (`flat_num`);

--
-- Constraints for table `leases_halls`
--
ALTER TABLE `leases_halls`
  ADD CONSTRAINT `leases_halls_ibfk_1` FOREIGN KEY (`grade_num`) REFERENCES `student` (`grade_num`),
  ADD CONSTRAINT `leases_halls_ibfk_2` FOREIGN KEY (`place_num`) REFERENCES `hall_rooms` (`place_num`),
  ADD CONSTRAINT `leases_halls_ibfk_3` FOREIGN KEY (`hall_num`) REFERENCES `hall_res` (`hall_num`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`advisor_id`) REFERENCES `advisor` (`advisor_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
