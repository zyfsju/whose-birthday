// import React from "react";
// import logo from "./logo.svg";
// import "./App.css";
import "react-calendar/dist/Calendar.css";
import PeopleContainer from "./PeopleContainer";
// function App() {
//   return (
//     <div className="App">
//       <header
//         onClick={(e) => {
//           console.log(e);
//           alert("hi");
//         }}
//         className="App-header"
//       >
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
// export default App;
import React, { Component } from "react";
import Calendar from "react-calendar";
import { Container } from "@material-ui/core";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import RecipeReviewCard from "./RecipeReviewCard";

export default class App extends Component {
  state = {
    date: new Date(),
    people: [],
    loading: false,
  };

  componentDidMount() {
    fetch("http://localhost:5000")
      .then((resp) => resp.json())
      .then((newPeople) => {
        this.setState({
          people: newPeople,
        });
      });
  }

  onChange = async (date) => {
    if (date.setHours(12, 0, 0, 0) === this.state.date.setHours(12, 0, 0, 0)) {
      return;
    }
    if (this.state.loading) {
      return;
    }
    this.setState({ date });
    let day = date.toISOString().split("T")[0];
    this.setState({ loading: true });
    const response = await fetch(`http://localhost:5000/mathematician/${day}`);
    const newPeople = await response.json();
    this.setState({ people: newPeople });
    this.setState({ loading: false });
  };
  render() {
    return (
      <Container minWidth="sm">
        <Grid
          container
          direction="row"
          justify="space-between"
          alignItems="stretch"
          spacing={3}
        >
          <Grid
            item
            xs={4}
            container
            direction="column"
            alignItems="stretch"
            spacing={2}
          >
            <Grid item>
              <Calendar onChange={this.onChange} value={this.state.date} />
            </Grid>{" "}
            <Grid item>
              <PeopleContainer
                people={this.state.people}
                loading={this.state.loading}
              />
            </Grid>
          </Grid>
          <Grid item xs={4}>
            <RecipeReviewCard />
          </Grid>
          <Grid item xs={4}>
            <RecipeReviewCard />
          </Grid>
        </Grid>
      </Container>
    );
  }
}

// <Box justifyContent="flex-start">…
// <Box justifyContent="flex-end">…
// <Box justifyContent="center">
// <Box
//   display="flex"
//   justifyContent="center"
//   m={1}
//   p={1}
//   bgcolor="background.paper"
// >
