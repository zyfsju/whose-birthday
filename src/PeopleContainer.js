import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import CircularProgress from "@material-ui/core/CircularProgress";

const useStyles = makeStyles({
  table: {
    minWidth: 200,
  },
  tableHeader: {
    // fontSize: "80pt",
    "font-weight": "bold",
  },
  spinner: { size: 60, color: "primary" },
});

function PeopleContainer(props) {
  const classes = useStyles();
  // TODO: pagination (make it as tall as calendar), sort, select -> move to card
  function renderPeople() {
    // console.log("People", typeof props.people);
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell className={classes.tableHeader}>Name</TableCell>
              <TableCell className={classes.tableHeader}>
                Date&nbsp;of&nbsp;Birth
              </TableCell>
              <TableCell className={classes.tableHeader}>Occupation</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.people &&
              props.people.map((person) => {
                return (
                  <TableRow key={person.Person}>
                    <TableCell component="th" scope="row">
                      {person.Person}
                    </TableCell>
                    <TableCell align="right">{person.Born}</TableCell>
                    <TableCell align="left">{person.occupation}</TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }

  return props.loading ? (
    <CircularProgress className={classes.spinner} />
  ) : (
    renderPeople()
  );
}

export default PeopleContainer;
