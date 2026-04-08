# Gurjas — Higher-Dimensional Visualization

##  Files

- `Gurjas/higher_dim_viz.py` — Main script
- `Gurjas/pca_visualization.png` — PCA projection of 5D feasible region
- `Gurjas/parallel_coordinates.png` — Parallel coordinates plot
- `Gurjas/correlation_heatmap.png` — Variable correlation heatmap
- `Gurjas/network_variable_distribution.png` — Japneet's network LP sparsity analysis

## How to Run

```bash
pip install scikit-learn scipy numpy matplotlib
python Gurjas/higher_dim_viz.py
```

##  Issues & Debugging Log

### Issue 1: Rejection sampling was extremely slow
When I first set up the feasible point sampler, I was generating random points across the full range `[0, 100]` for each variable. Almost none of them landed inside the polytope, so the script would hang trying to get 500 points. I fixed this by computing a tighter upper bound per variable using `b[i] / A[i,j]` so the random draws stay within a reasonable box. Went from ~500k attempts down to ~9k.

### Issue 2: PCA plot had no color variation
Initially I forgot to color the scatter plot by objective value — everything was just blue dots and the plot looked meaningless. After adding `c=obj_vals` with a viridis colormap and a colorbar, you can actually see the gradient from low-z (purple) to high-z (yellow) and the optimal point stands out clearly.

### Issue 3: Parallel coordinates — all lines overlapping
With 500 lines drawn at full opacity the plot was an unreadable mess. I reduced it to 200 randomly sampled lines at `alpha=0.25` which made the patterns visible while still showing the distribution. Also normalized each axis to `[0, 1]` so variables with different scales didn't dominate.

### Issue 4: Path issues reading Japneet's MPS file
Japneet's data lives at `Japneet/Japneet/data/long15.mps` (nested folder), but I initially looked for it at `Japneet/data/long15.mps`. The script kept printing "file not found." I added multiple candidate paths to handle both cases so it works regardless of which path exists.

### Issue 5: MPS parsing was too slow
The `long15.mps` file is 3 million lines. Parsing the entire COLUMNS section took over a minute. I capped it at 200k column lines which still captures all 66,667 unique variables but runs in a few seconds.

---

## References

### YouTube Videos

- Joshua Emmanuel. (2022, August 17).
  *Intro to simplex method | Solve LP | Simplex tableau* [Video]. YouTube.
  🔗 https://www.youtube.com/watch?v=9YKLXFqCy6E

- Tom S. (2023).
  *The art of linear programming* [Video]. YouTube.
  🔗 https://www.youtube.com/watch?v=E72DWgKP_1Y

### Documentation & Tutorials

- scikit-learn developers. (2024).
  *PCA — Principal Component Analysis*. scikit-learn Documentation.
  🔗 https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

- SciPy developers. (2024).
  *scipy.optimize.linprog — Linear programming*. SciPy Documentation.
  🔗 https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

- Mittelmann, H. (2026).
  *Large Network-LP Benchmark (commercial vs free)*.
  🔗 https://plato.asu.edu/ftp/lptestset/network/
  Benchmark plots: https://mattmilten.github.io/mittelmann-plots/

### Software & Tools

- Microsoft. (2024).
  *Visual Studio Code* [Computer software].
  🔗 https://code.visualstudio.com/
  📄 License: MIT License (Code - OSS) / Proprietary (official distribution)

- Anthropic. (2025).
  *Claude* [AI assistant].
  🔗 https://claude.ai/
  Used for debugging assistance, code review, and understanding PCA loadings interpretation.

- Python Software Foundation. (2024).
  *Python 3.12* [Programming language].
  🔗 https://www.python.org/

### Academic References

- Jolliffe, I. T., & Cadima, J. (2016).
  Principal component analysis: a review and recent developments.
  *Philosophical Transactions of the Royal Society A*, 374(2065), 20150202.
  🔗 https://doi.org/10.1098/rsta.2015.0202

- Inselberg, A. (2009).
  *Parallel Coordinates: Visual Multidimensional Geometry and Its Applications*. Springer.

---

## AI Usage Disclosure

Claude (Anthropic) was used during development for:
- Debugging the rejection sampling performance issue
- Reviewing matplotlib plotting code for parallel coordinates
- Suggesting the PCA loadings annotation box approach
- Helping interpret correlation patterns in the heatmap output

All final code was reviewed, understood, and tested by me before submission.
